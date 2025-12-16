from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.session import SessionState
from app.config import settings
from app import db
import datetime

app = FastAPI(title=settings.APP_NAME)

active_sessions: dict[str, SessionState] = {}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws/session/{session_id}")
async def websocket_session(websocket: WebSocket, session_id: str):
    await websocket.accept()

    session = SessionState(session_id)
    active_sessions[session_id] = session

    # Persist session start
    db.create_session(session_id)

    print(f"[CONNECT] {session_id}")

    try:
        while True:
            user_message = await websocket.receive_text()

            session.add_message("user", user_message)
            db.log_event(session_id, "user", user_message)

            response = f"Received: {user_message}"

            session.add_message("assistant", response)
            db.log_event(session_id, "assistant", response)

            await websocket.send_text(response)

    except WebSocketDisconnect:
        end_time = datetime.datetime.utcnow()
        duration = int((end_time - session.start_time).total_seconds())

        db.close_session(session_id, end_time, duration)

        print(f"[DISCONNECT] {session_id} ({duration}s)")

        active_sessions.pop(session_id, None)
