from fastapi import APIRouter

from app.ai.rag.rag_service import RAGService
from app.schemas.chat import (ChatRequest,ChatResponse,)

router = APIRouter(prefix="/chat",tags=["Chat"],)
rag = RAGService()

from fastapi import HTTPException

@router.post("",response_model=ChatResponse,)
def chat(request: ChatRequest,):
    print(request)
    try:
        return rag.ask(request.session_id, request.question, request.document_id)
    except Exception as e:
        detail = str(e)
        if "403" in detail or "Forbidden" in detail or "Authorization" in detail:
            raise HTTPException(status_code=401, detail="NVIDIA API Authorization Failed. Please check your NVIDIA API key in Settings.")
        raise HTTPException(status_code=400, detail=f"Error: {detail}")