import datetime

class SessionState:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.start_time = datetime.datetime.utcnow()
        self.messages = []  # chronological message history

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
