from collections import defaultdict


class ConversationMemory:

    def __init__(self):
        self.memory = defaultdict(list)

    def add(
        self,
        session_id: str,
        role: str,
        message: str,
    ):
        self.memory[session_id].append(
            {
                "role": role,
                "content": message,
            }
        )

    def history(
        self,
        session_id: str,
        limit: int = 10,
    ):
        return self.memory[session_id][-limit:]