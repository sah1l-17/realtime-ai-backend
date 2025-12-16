from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.config import settings
from app.session import SessionState
import datetime

app = FastAPI(title=settings.APP_NAME)

# In-memory session store
active_sessions: dict[str, SessionState] = {}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws/session/{session_id}")
async def websocket_session(websocket: WebSocket, session_id: str):
    await websocket.accept()

    # Create session state
    session = SessionState(session_id)
    active_sessions[session_id] = session

    print(f"[CONNECT] Session {session_id} started at {session.start_time}")

    try:
        while True:
            user_message = await websocket.receive_text()

            # Save user message
            session.add_message("user", user_message)

            print(f"[USER] {session_id}: {user_message}")

            # Temporary echo response
            response = f"Received: {user_message}"
            session.add_message("assistant", response)

            await websocket.send_text(response)

    except WebSocketDisconnect:
        end_time = datetime.datetime.utcnow()
        duration = (end_time - session.start_time).total_seconds()

        print(f"[DISCONNECT] Session {session_id}")
        print(f"Duration: {duration} seconds")
        print(f"Messages exchanged: {len(session.messages)}")

        # Cleanup
        active_sessions.pop(session_id, None)
