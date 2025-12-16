import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_session(session_id: str, user_id: str = "anonymous"):
    supabase.table("sessions").insert({
        "session_id": session_id,
        "user_id": user_id
    }).execute()


def log_event(session_id: str, event_type: str, content: str):
    supabase.table("session_events").insert({
        "session_id": session_id,
        "event_type": event_type,
        "content": content
    }).execute()


def close_session(session_id: str, end_time, duration_seconds: int):
    supabase.table("sessions").update({
        "end_time": end_time,
        "duration_seconds": duration_seconds
    }).eq("session_id", session_id).execute()
