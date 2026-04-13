"""
Chat API endpoints.
Detects booking intent from the AI response and auto-books via Cal.com API.
"""
import re
import json
import uuid
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from ..config import get_settings
from ..rag.runtime import ensure_runtime_ready, get_runtime_state

router = APIRouter(prefix="/api/chat", tags=["chat"])

CAL_API_BASE = "https://api.cal.com/v2"
IST = ZoneInfo("Asia/Kolkata")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None


class BookingInfo(BaseModel):
    success: bool
    booking_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    meeting_url: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    response: str
    session_id: str
    booking: Optional[BookingInfo] = None


class ResetRequest(BaseModel):
    session_id: str


class ResetResponse(BaseModel):
    success: bool
    message: str


# ── Booking Logic ──────────────────────────────────────────────

BOOK_MEETING_PATTERN = re.compile(
    r'\[BOOK_MEETING\](.*?)\[/BOOK_MEETING\]',
    re.DOTALL
)


def _normalize_booking_datetime(local_dt: datetime, now_ist: datetime) -> datetime:
    """Shift stale model-generated years to the next valid future occurrence."""
    if local_dt > now_ist or local_dt.year >= now_ist.year:
        return local_dt

    for year in (now_ist.year, now_ist.year + 1):
        try:
            candidate = local_dt.replace(year=year)
        except ValueError:
            continue
        if candidate > now_ist:
            return candidate

    return local_dt


async def _attempt_booking(booking_data: dict) -> BookingInfo:
    """Call Cal.com API to create a booking."""
    settings = get_settings()

    if not settings.CAL_COM_API_KEY or not settings.CAL_COM_EVENT_TYPE_ID:
        return BookingInfo(
            success=False,
            message="Calendar API not configured.",
        )

    name = booking_data.get("name", "")
    email = booking_data.get("email", "")
    date = booking_data.get("date", "")
    time_str = booking_data.get("time", "10:00")

    if not name or not email or not date:
        return BookingInfo(
            success=False,
            message="Missing required booking details (name, email, or date).",
        )

    try:
        local_dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M").replace(
            tzinfo=IST
        )
    except ValueError:
        return BookingInfo(
            success=False,
            message=f"Invalid date/time format: {date} {time_str}",
        )

    now_ist = datetime.now(IST)
    local_dt = _normalize_booking_datetime(local_dt, now_ist)
    booking_data["date"] = local_dt.strftime("%Y-%m-%d")
    booking_data["time"] = local_dt.strftime("%H:%M")

    if local_dt <= now_ist:
        now_display = now_ist.strftime("%Y-%m-%d %H:%M IST")
        requested_display = local_dt.strftime("%Y-%m-%d %H:%M IST")
        return BookingInfo(
            success=False,
            message=(
                f"The requested slot {requested_display} is in the past. "
                f"Please choose a future time after {now_display}."
            ),
        )

    start_utc = local_dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        "start": start_utc,
        "eventTypeId": settings.CAL_COM_EVENT_TYPE_ID,
        "attendee": {
            "name": name,
            "email": email,
            "timeZone": "Asia/Kolkata",
        },
    }

    headers = {
        "Authorization": f"Bearer {settings.CAL_COM_API_KEY}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-08-13",
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{CAL_API_BASE}/bookings",
                json=payload,
                headers=headers,
                timeout=15,
            )

        if resp.status_code not in (200, 201):
            error_msg = resp.text
            try:
                error_msg = resp.json().get("message", error_msg)
            except Exception:
                pass
            return BookingInfo(
                success=False,
                message=f"Booking failed: {error_msg}",
            )

        data = resp.json().get("data", resp.json())
        booking_id = data.get("uid", data.get("id", ""))
        start_time = data.get("startTime", data.get("start", start_utc))
        end_time = data.get("endTime", data.get("end", ""))

        meeting_url = None
        if data.get("metadata", {}).get("videoCallUrl"):
            meeting_url = data["metadata"]["videoCallUrl"]
        elif data.get("meetingUrl"):
            meeting_url = data["meetingUrl"]
        elif data.get("references"):
            for ref in data["references"]:
                if ref.get("meetingUrl"):
                    meeting_url = ref["meetingUrl"]
                    break

        return BookingInfo(
            success=True,
            booking_id=str(booking_id),
            start_time=start_time,
            end_time=end_time,
            meeting_url=meeting_url,
            message=f"Meeting booked for {name} ({email}) on {date} at {time_str}",
        )

    except Exception as e:
        return BookingInfo(
            success=False,
            message=f"Booking error: {str(e)}",
        )


# ── Endpoints ──────────────────────────────────────────────────

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to Utkersh's AI persona and get a response."""
    try:
        state = await ensure_runtime_ready()
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="AI persona is not initialized. Please run the ingestion script first.",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"AI persona is still loading or failed to initialize: {exc}",
        )

    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())

    try:
        response = await state.persona_chat.chat(session_id, request.message)

        # Check if the AI wants to book a meeting
        booking_info = None
        match = BOOK_MEETING_PATTERN.search(response)
        if match:
            try:
                booking_data = json.loads(match.group(1).strip())
                booking_info = await _attempt_booking(booking_data)

                # Replace the tag in the response with the booking result
                if booking_info.success:
                    booking_msg = (
                        f"✅ **Meeting booked!**\n"
                        f"- **When:** {booking_data.get('date')} at {booking_data.get('time')}\n"
                        f"- **Attendee:** {booking_data.get('name')} ({booking_data.get('email')})\n"
                    )
                    if booking_info.meeting_url:
                        booking_msg += f"- **Meeting link:** {booking_info.meeting_url}\n"
                    booking_msg += "\nYou should receive a confirmation email shortly!"
                else:
                    booking_msg = (
                        f"⚠️ I tried to book the meeting, but ran into an issue: "
                        f"{booking_info.message}. "
                        f"You can also book manually at: {get_settings().CAL_COM_LINK}"
                    )

                response = BOOK_MEETING_PATTERN.sub(booking_msg, response)

            except json.JSONDecodeError:
                # If the JSON is malformed, just clean the tag
                response = BOOK_MEETING_PATTERN.sub("", response)

        return ChatResponse(
            response=response,
            session_id=session_id,
            booking=booking_info,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.post("/reset", response_model=ResetResponse)
async def reset_session(request: ResetRequest):
    """Reset conversation history for a session."""
    state = get_runtime_state()
    if state.persona_chat is None:
        raise HTTPException(status_code=503, detail="AI persona not initialized.")

    success = state.persona_chat.reset_session(request.session_id)
    return ResetResponse(
        success=success,
        message="Session reset successfully." if success else "Session not found.",
    )
