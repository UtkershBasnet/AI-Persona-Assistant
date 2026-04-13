"""
Vapi-compatible OpenAI endpoint.

Vapi sends POST requests in OpenAI Chat Completions format.
We intercept them, inject RAG context, forward to Groq (fast model),
and stream the response back in SSE format.

Flow: Caller → Vapi (STT) → this endpoint → RAG + Groq → Vapi (TTS) → Caller
"""
import json
import re
import time
import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator
from zoneinfo import ZoneInfo

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from groq import Groq

from ..config import get_settings
from ..rag.runtime import ensure_runtime_ready, get_runtime_state

router = APIRouter(prefix="/api/vapi", tags=["vapi"])

CAL_API_BASE = "https://api.cal.com/v2"
BOOK_MEETING_PATTERN = re.compile(r'\[BOOK_MEETING\](.*?)\[/BOOK_MEETING\]', re.DOTALL)
IST = ZoneInfo("Asia/Kolkata")

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


VOICE_SYSTEM_PROMPT = """\
You are Utkersh Basnet's AI phone representative. Speak naturally and conversationally as Utkersh in first person.

CRITICAL: This is a PHONE CALL. Keep every response to 2-4 sentences MAX. Be concise and natural.

Use the following context from Utkersh's resume and GitHub repos to answer:
{context}

Today's date in Asia/Kolkata is {current_date}.

Rules:
- Be friendly, warm, and enthusiastic — like talking to a colleague
- Keep answers SHORT and punchy — nobody reads essays on a phone call
- If you don't know something, say: "I don't have that info handy, but we can definitely cover it in a proper call. Want to book some time?"
- Never hallucinate or make up information not in the context
- Use natural speech patterns — contractions, filler words are OK
- Don't use markdown, bullet points, or formatting — this is spoken audio
- Don't say "according to my context" or "based on the provided information" — just answer naturally

## Booking Meetings:
When a caller wants to schedule a meeting:
1. Ask for their full name
2. Ask for their email address
3. Ask what day and time works for them
3a. If they mention a month/day without a year, assume the next future occurrence in Asia/Kolkata.
4. Once you have all three, say "Let me book that for you right now" and include this exact tag in your response:
   [BOOK_MEETING]{{"name": "Their Name", "email": "their@email.com", "date": "YYYY-MM-DD", "time": "HH:MM"}}[/BOOK_MEETING]
5. Then say "All set! You should get a confirmation email shortly."
"""


def _retrieve_context(query: str) -> str:
    """Retrieve relevant document chunks for RAG."""
    retriever = get_runtime_state().retriever
    if not retriever:
        return "No context available."

    docs = retriever.invoke(query, k=4)
    if not docs:
        return "No specific context found."

    parts = []
    for doc in docs:
        source = doc.metadata.get("source_name", "Unknown")
        parts.append(f"[{source}] {doc.page_content}")

    return "\n\n".join(parts)


def _build_enriched_messages(messages: list, context: str, cal_link: str) -> list:
    """Replace/inject the system prompt with RAG-enriched context."""
    system_prompt = VOICE_SYSTEM_PROMPT.format(
        context=context,
        current_date=datetime.now(IST).strftime("%Y-%m-%d"),
    )

    enriched = [{"role": "system", "content": system_prompt}]

    # Add conversation history, skipping Vapi's original system message
    for msg in messages:
        if msg.get("role") == "system":
            continue  # Skip Vapi's system prompt, we use our own
        # Only include text content
        content = msg.get("content", "")
        if isinstance(content, list):
            # Vapi sometimes sends content as a list of objects
            text_parts = [
                p.get("text", "") for p in content
                if isinstance(p, dict) and p.get("type") == "text"
            ]
            content = " ".join(text_parts)
        if content:
            enriched.append({"role": msg["role"], "content": content})

    return enriched


async def _fire_booking(booking_data: dict):
    """Fire a Cal.com booking in the background (best-effort)."""
    settings = get_settings()
    if not settings.CAL_COM_API_KEY or not settings.CAL_COM_EVENT_TYPE_ID:
        return

    name = booking_data.get("name", "")
    email = booking_data.get("email", "")
    date = booking_data.get("date", "")
    time_str = booking_data.get("time", "10:00")

    if not name or not email or not date:
        return

    try:
        local_dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M").replace(
            tzinfo=IST
        )
    except ValueError:
        return

    local_dt = _normalize_booking_datetime(local_dt, datetime.now(IST))

    if local_dt <= datetime.now(IST):
        return

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

    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{CAL_API_BASE}/bookings",
                json=payload,
                headers={
                    "Authorization": f"Bearer {settings.CAL_COM_API_KEY}",
                    "Content-Type": "application/json",
                    "cal-api-version": "2024-08-13",
                },
                timeout=15,
            )
    except Exception:
        pass  # Best-effort — don't break the call


def _clean_response_and_extract_booking(content: str) -> tuple[str, dict | None]:
    """Strip [BOOK_MEETING] tags and extract booking data."""
    match = BOOK_MEETING_PATTERN.search(content)
    if not match:
        return content, None

    try:
        booking_data = json.loads(match.group(1).strip())
    except json.JSONDecodeError:
        booking_data = None

    cleaned = BOOK_MEETING_PATTERN.sub("", content).strip()
    return cleaned, booking_data


@router.post("/chat/completions")
async def chat_completions(request: Request):
    """
    OpenAI-compatible chat completions endpoint for Vapi.
    Vapi POSTs here with conversation history, we do RAG + Groq, stream back.
    Booking tags are stripped so they're never spoken by TTS.
    """
    body = await request.json()
    messages = body.get("messages", [])
    is_stream = body.get("stream", True)

    try:
        await ensure_runtime_ready()
    except Exception:
        pass

    # Extract the last user message for RAG retrieval
    last_user_msg = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, list):
                text_parts = [
                    p.get("text", "") for p in content
                    if isinstance(p, dict) and p.get("type") == "text"
                ]
                content = " ".join(text_parts)
            last_user_msg = content
            break

    # RAG retrieval
    context = _retrieve_context(last_user_msg) if last_user_msg else ""

    # Build enriched messages with RAG context
    settings = get_settings()
    enriched_messages = _build_enriched_messages(
        messages, context, settings.CAL_COM_LINK
    )

    # Create Groq client — get FULL response first (fast with 8B model)
    client = Groq(api_key=settings.GROQ_API_KEY)

    response = client.chat.completions.create(
        model=settings.VOICE_MODEL,
        messages=enriched_messages,
        stream=False,
        temperature=0.4,
        max_tokens=250,
    )

    raw_content = response.choices[0].message.content
    cleaned_content, booking_data = _clean_response_and_extract_booking(raw_content)

    # Fire booking in background if detected
    if booking_data:
        import asyncio
        asyncio.create_task(_fire_booking(booking_data))

    completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())

    if is_stream:
        # Stream the cleaned content as SSE chunks
        async def generate():
            # First chunk: role
            yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': created, 'model': settings.VOICE_MODEL, 'choices': [{'index': 0, 'delta': {'role': 'assistant'}, 'finish_reason': None}]})}\n\n"

            # Stream content word by word for natural TTS pacing
            words = cleaned_content.split(" ")
            for i, word in enumerate(words):
                token = word if i == 0 else f" {word}"
                chunk = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": settings.VOICE_MODEL,
                    "choices": [{"index": 0, "delta": {"content": token}, "finish_reason": None}],
                }
                yield f"data: {json.dumps(chunk)}\n\n"

            # Final chunk
            yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': created, 'model': settings.VOICE_MODEL, 'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    else:
        return {
            "id": completion_id,
            "object": "chat.completion",
            "created": created,
            "model": settings.VOICE_MODEL,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": cleaned_content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }
