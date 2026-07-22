from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import BackgroundTasks
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
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return DocumentService.upload(db,current_user,file,background_tasks)