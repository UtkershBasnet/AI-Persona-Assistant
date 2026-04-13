"""
Calendar API — Automated booking via Cal.com API v2.

Endpoints:
  GET  /api/calendar/slots   — Fetch available time slots for a given date range
  POST /api/calendar/book    — Create a booking (fully automated, no redirect)
  GET  /api/calendar/link    — Fallback Cal.com link
"""
import httpx
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr

from ..config import get_settings

router = APIRouter(prefix="/api/calendar", tags=["calendar"])

CAL_API_BASE = "https://api.cal.com/v2"


# ── Request / Response Models ──────────────────────────────────

class BookingRequest(BaseModel):
    name: str
    email: str
    start: str  # ISO 8601 UTC, e.g. "2026-04-14T09:00:00Z"
    timeZone: str = "Asia/Kolkata"
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    success: bool
    booking_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    meeting_url: Optional[str] = None
    message: str


class SlotResponse(BaseModel):
    date: str
    slots: list[str]  # List of ISO 8601 start times


# ── Helpers ─────────────────────────────────────────────────────

def _cal_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


# ── Endpoints ───────────────────────────────────────────────────

@router.get("/slots")
async def get_available_slots(
    start_date: str = Query(
        ..., description="Start date YYYY-MM-DD", example="2026-04-14"
    ),
    end_date: Optional[str] = Query(
        None, description="End date YYYY-MM-DD (defaults to start_date + 3 days)"
    ),
    timeZone: str = Query("Asia/Kolkata", description="IANA timezone"),
):
    """Fetch available booking slots from Cal.com."""
    settings = get_settings()

    if not settings.CAL_COM_API_KEY or not settings.CAL_COM_EVENT_TYPE_ID:
        raise HTTPException(
            status_code=503,
            detail="Cal.com API not configured. Set CAL_COM_API_KEY and CAL_COM_EVENT_TYPE_ID in .env",
        )

    # Default end_date to start + 3 days
    if not end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=3)
        end_date = end_dt.strftime("%Y-%m-%d")

    params = {
        "eventTypeId": settings.CAL_COM_EVENT_TYPE_ID,
        "start": start_date,
        "end": end_date,
        "timeZone": timeZone,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{CAL_API_BASE}/slots",
            params=params,
            headers={
                **_cal_headers(settings.CAL_COM_API_KEY),
                "cal-api-version": "2024-09-04",
            },
            timeout=15,
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Cal.com API error: {resp.text}",
        )

    data = resp.json()
    slots_data = data.get("data", {}).get("slots", {})

    # Flatten into a cleaner format
    result = []
    for date_key, day_slots in slots_data.items():
        times = [slot.get("time", slot) if isinstance(slot, dict) else slot for slot in day_slots]
        result.append({"date": date_key, "slots": times})

    return {
        "available_slots": result,
        "event_type_id": settings.CAL_COM_EVENT_TYPE_ID,
        "timezone": timeZone,
    }


@router.post("/book", response_model=BookingResponse)
async def create_booking(booking: BookingRequest):
    """
    Create a confirmed booking on Cal.com — fully automated.
    No human intervention needed.
    """
    settings = get_settings()

    if not settings.CAL_COM_API_KEY or not settings.CAL_COM_EVENT_TYPE_ID:
        raise HTTPException(
            status_code=503,
            detail="Cal.com API not configured.",
        )

    payload = {
        "start": booking.start,
        "eventTypeId": settings.CAL_COM_EVENT_TYPE_ID,
        "attendee": {
            "name": booking.name,
            "email": booking.email,
            "timeZone": booking.timeZone,
        },
    }

    if booking.notes:
        payload["metadata"] = {"notes": booking.notes}

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{CAL_API_BASE}/bookings",
            json=payload,
            headers={
                **_cal_headers(settings.CAL_COM_API_KEY),
                "cal-api-version": "2024-08-13",
            },
            timeout=15,
        )

    if resp.status_code not in (200, 201):
        error_detail = resp.text
        try:
            error_json = resp.json()
            error_detail = error_json.get("message", error_detail)
        except Exception:
            pass

        return BookingResponse(
            success=False,
            message=f"Booking failed: {error_detail}",
        )

    data = resp.json().get("data", resp.json())

    # Extract booking details
    booking_id = data.get("uid", data.get("id", ""))
    start_time = data.get("startTime", data.get("start", booking.start))
    end_time = data.get("endTime", data.get("end", ""))

    # Try to get meeting URL (for video calls)
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

    return BookingResponse(
        success=True,
        booking_id=str(booking_id),
        start_time=start_time,
        end_time=end_time,
        meeting_url=meeting_url,
        message=f"Meeting booked successfully with {booking.name} ({booking.email})",
    )


@router.get("/link")
async def get_calendar_link():
    """Fallback — get the manual booking link."""
    settings = get_settings()
    return {
        "link": settings.CAL_COM_LINK,
        "provider": "cal.com",
    }
