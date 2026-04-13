/**
 * API client for the AI Persona backend.
 */

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "https://ai-persona-assistant.onrender.com";

export interface BookingInfo {
  success: boolean;
  booking_id?: string;
  start_time?: string;
  end_time?: string;
  meeting_url?: string;
  message: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  booking?: BookingInfo | null;
}

export interface SlotData {
  date: string;
  slots: string[];
}

export interface SlotsResponse {
  available_slots: SlotData[];
  event_type_id: number;
  timezone: string;
}

export interface CalendarLinkResponse {
  link: string;
  provider: string;
}

/**
 * Send a chat message to the AI persona.
 */
export async function sendMessage(
  message: string,
  sessionId?: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      session_id: sessionId || null,
    }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `API error: ${res.status}`);
  }

  return res.json();
}

/**
 * Reset a chat session.
 */
export async function resetSession(sessionId: string): Promise<void> {
  await fetch(`${API_BASE}/api/chat/reset`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });
}

/**
 * Get available booking slots for a date range.
 */
export async function getAvailableSlots(
  startDate: string,
  endDate?: string,
  timeZone: string = "Asia/Kolkata"
): Promise<SlotsResponse> {
  const params = new URLSearchParams({
    start_date: startDate,
    timeZone,
  });
  if (endDate) params.append("end_date", endDate);

  const res = await fetch(`${API_BASE}/api/calendar/slots?${params}`);
  if (!res.ok) throw new Error("Failed to fetch available slots");
  return res.json();
}

/**
 * Create a booking directly via Cal.com API.
 */
export async function createBooking(
  name: string,
  email: string,
  startTime: string,
  timeZone: string = "Asia/Kolkata",
  notes?: string
): Promise<BookingInfo> {
  const res = await fetch(`${API_BASE}/api/calendar/book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      email,
      start: startTime,
      timeZone,
      notes,
    }),
  });

  if (!res.ok) throw new Error("Booking request failed");
  return res.json();
}

/**
 * Get the calendar booking link (fallback).
 */
export async function getCalendarLink(): Promise<CalendarLinkResponse> {
  const res = await fetch(`${API_BASE}/api/calendar/link`);
  if (!res.ok) throw new Error("Failed to fetch calendar link");
  return res.json();
}

/**
 * Health check.
 */
export async function healthCheck(): Promise<{ status: string; rag_initialized: boolean }> {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}
