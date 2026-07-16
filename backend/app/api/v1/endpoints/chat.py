from fastapi import APIRouter

from app.ai.rag.rag_service import RAGService
from app.schemas.chat import (ChatRequest,ChatResponse,)

router = APIRouter(prefix="/chat",tags=["Chat"],)
rag = RAGService()

@router.post("",response_model=ChatResponse,)
def chat(request: ChatRequest,):
    print(request)
    return rag.ask(request.session_id, request.question)