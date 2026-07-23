from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import BackgroundTasks
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.api.deps import get_db
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.models.document import Document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.get("", response_model=list[DocumentResponse])
def list_documents(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Document).filter(Document.user_id == current_user.id).all()

@router.post("/upload",response_model=DocumentResponse,)
def upload_document(
    file: UploadFile = File(...),
    project_id: UUID | None = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return DocumentService.upload(db,current_user,file,background_tasks,project_id)

@router.delete("/{document_id}")
def delete_document(
    document_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        DocumentService.delete(db, doc)
    except Exception as e:
        detail = str(e)
        if "403" in detail or "Forbidden" in detail or "Authorization" in detail:
            raise HTTPException(status_code=401, detail="NVIDIA API Authorization Failed. Please check your NVIDIA API key in Settings.")
        raise HTTPException(status_code=400, detail=f"Failed to delete document: {detail}")
    return {"message": "Document deleted successfully"}