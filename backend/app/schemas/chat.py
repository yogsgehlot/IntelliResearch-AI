from pydantic import BaseModel

class ChatRequest(BaseModel):
    # project_id: str
    session_id: str = "default"
    question: str
    document_id: str | None = None

class ChatResponse(BaseModel):
    answer: str
    sources: list
