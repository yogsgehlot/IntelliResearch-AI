from pydantic import BaseModel

class ChatRequest(BaseModel):
    # project_id: str
    session_id: str = "default"
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list
