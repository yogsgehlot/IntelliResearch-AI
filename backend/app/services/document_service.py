from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.ai.processor import DocumentProcessor
from app.models.document import Document, DocumentStatus
from app.repositories.document_repository import DocumentRepository
from app.storage.storage_service import storage
from app.utils.file_utils import (generate_filename,validate_extension,)

class DocumentService:
    @staticmethod
    def upload(db: Session,user,file: UploadFile,):
        extension = validate_extension(file.filename)
        filename = generate_filename(file.filename)
        storage_path = storage.save(file,filename,)
        document = Document(
            user_id=user.id,
            filename=filename,
            original_name=file.filename,
            mime_type=file.content_type,
            extension=extension,
            file_size=file.size,
            storage_path=storage_path,
            status=DocumentStatus.PROCESSING,
        )

        document = DocumentRepository.create(db,document,)
        DocumentProcessor.process(db,document,)
        return document