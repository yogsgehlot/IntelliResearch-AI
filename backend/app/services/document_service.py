from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.orm import Session
from app.ai.processor import DocumentProcessor
from app.models.document import Document, DocumentStatus
from app.repositories.document_repository import DocumentRepository
from app.storage.storage_service import storage
from app.utils.file_utils import (generate_filename,validate_extension,)

class DocumentService:
    @staticmethod
    def upload(db: Session, user, file: UploadFile, background_tasks: BackgroundTasks):
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
        background_tasks.add_task(DocumentProcessor.process, document.id)
        return document

    @staticmethod
    def delete(db: Session, document: Document):
        # 1. Delete file from storage
        if document.storage_path:
            storage.delete(document.storage_path)

        # 2. Delete document from database (cascades to chunks)
        db.delete(document)
        db.commit()

        # 3. Rebuild vector store to keep metadata/FAISS in sync
        DocumentService.rebuild_vector_store(db)

    @staticmethod
    def rebuild_vector_store(db: Session):
        import os
        from app.ai.vectorstore.faiss_store import FaissStore
        from app.ai.vectorstore.metadata_store import MetadataStore
        from app.ai.embedding.embedding_service import EmbeddingService

        # Reset FAISS index file
        if FaissStore.INDEX_PATH.exists():
            try:
                os.remove(FaissStore.INDEX_PATH)
            except Exception:
                pass

        vector_store = FaissStore()
        metadata_store = MetadataStore()
        embedding_service = EmbeddingService()

        ready_docs = db.query(Document).filter(Document.status == DocumentStatus.READY).all()
        new_metadata = []

        for doc in ready_docs:
            for chunk in doc.chunks:
                vector = embedding_service.embed_text(chunk.content)
                vector_store.add(vector.reshape(1, -1))
                new_metadata.append({
                    "document_id": str(doc.id),
                    "document_name": doc.original_name,
                    "page": None,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "language": doc.language,
                    "tokens": chunk.token_count,
                    "project_id": str(doc.project_id) if doc.project_id else None,
                })

        metadata_store.save(new_metadata)

        # Reload global container
        import app.core.ai_container as container
        if container.ai_container is not None:
            container.ai_container.metadata = new_metadata
            container.ai_container.bm25.build(new_metadata)
            container.ai_container.faiss = FaissStore()