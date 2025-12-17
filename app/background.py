from app import db
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_session_summary(session_id: str):
    events = db.supabase.table("session_events") \
        .select("event_type, content") \
        .eq("session_id", session_id) \
        .execute()

    conversation = "\n".join(
        f"{e['event_type']}: {e['content']}"
        for e in events.data
    )

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Summarize this conversation briefly."},
            {"role": "user", "content": conversation}
        ]
    )

    summary = completion.choices[0].message.content

    db.supabase.table("sessions").update({
        "summary": summary
    }).eq("session_id", session_id).execute()
