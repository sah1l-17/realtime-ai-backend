# Realtime AI Backend (WebSockets + Supabase)

## Overview
A real-time AI backend that streams LLM responses over WebSockets, maintains session state, persists conversation data in Supabase, supports LLM tool calling, and generates automated post-session summaries.

The focus is on **backend architecture, async design, and real-time systems**.

---

## Features
- Realtime WebSocket communication
- Token-by-token LLM streaming (Groq)
- Stateful multi-turn conversations
- LLM tool/function calling
- Persistent session & event logging (Supabase)
- Post-session automated summary generation

---

## Tech Stack
- **Backend:** FastAPI (async)
- **Realtime:** WebSockets
- **LLM:** Groq (LLaMA 3)
- **Database:** Supabase (PostgreSQL)
- **Frontend:** Minimal HTML/CSS/JS

---

## Database Schema (Supabase)

```sql
create table if not exists sessions (
    session_id text primary key,
    user_id text,
    start_time timestamp,
    end_time timestamp,
    duration_seconds integer,
    summary text
);

create table if not exists session_events (
    id uuid primary key default gen_random_uuid(),
    session_id text references sessions(session_id),
    event_type text,
    content text,
    timestamp timestamp default now()
);


create index if not exists idx_session_events_session_time
on session_events (session_id, timestamp);

```
## Environment Variables
Create a .env file:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-8b-8192
```

## Setup & Run
```bash
git clone https://github.com/your-username/realtime-ai-backend.git
cd realtime-ai-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Server runs at:
```
http://127.0.0.1:8000
```

## How It Works

Client connects via WebSocket

Backend generates a unique session ID

Messages stream token-by-token from the LLM

All events are stored in Supabase

On disconnect, a background task generates a session summary

## Notes
Frontend is intentionally minimal to emphasize backend behavior

Row Level Security (RLS) is disabled for demo simplicity

Designed to demonstrate production-style real-time AI systems
