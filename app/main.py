from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.session import SessionState
from app.config import settings
from app import db
from app.llm import stream_chat_completion
import datetime
import uuid

app = FastAPI(title=settings.APP_NAME)

# In-memory active sessions
active_sessions: dict[str, SessionState] = {}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws/session")
async def websocket_session(websocket: WebSocket):
    await websocket.accept()

    # Generate unique session ID per connection
    session_id = str(uuid.uuid4())

    # Create session state
    session = SessionState(session_id)
    active_sessions[session_id] = session

    # Persist session start
    db.create_session(session_id)

    print(f"[CONNECT] {session_id}")

    # Optional: send session_id to client
    await websocket.send_text(f"[SESSION_ID]{session_id}")

    try:
        while True:
            user_message = await websocket.receive_text()

            # Log user message
            session.add_message("user", user_message)
            db.log_event(session_id, "user", user_message)

            full_response = ""

            # Stream AI tokens
            async for token in stream_chat_completion(session.get_llm_messages()):
                full_response += token
                await websocket.send_text(token)

            # Log AI response
            session.add_message("assistant", full_response)
            db.log_event(session_id, "assistant", full_response)

    except WebSocketDisconnect:
        end_time = datetime.datetime.utcnow()
        duration = int((end_time - session.start_time).total_seconds())

        # Persist session end
        db.close_session(session_id, end_time, duration)

        active_sessions.pop(session_id, None)

        print(f"[DISCONNECT] {session_id} ({duration}s)")
