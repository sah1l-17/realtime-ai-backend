import datetime

class SessionState:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.start_time = datetime.datetime.utcnow()
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_llm_messages(self):
        return self.messages
