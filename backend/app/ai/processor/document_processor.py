from uuid import UUID
from app.database.session import SessionLocal
from app.core.logger import logger
from app.ai.chunking.chunker import TextChunker
from app.ai.parser.parser_factory import ParserFactory
from app.ai.preprocessing.cleaner import TextCleaner
from app.ai.preprocessing.language import LanguageDetector
from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.ai.embedding.embedding_service import EmbeddingService
from app.ai.vectorstore.faiss_store import FaissStore
from app.ai.vectorstore.metadata_store import MetadataStore


import threading

class DocumentProcessor:
    _lock = threading.Lock()

    @staticmethod
    def process(document_id: UUID) -> None:
        db = SessionLocal()
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                logger.error(f"Document {document_id} not found during processing")
                return

            document.status = DocumentStatus.PROCESSING
            db.commit()

            parser = ParserFactory.get_parser(document.extension)
            text = parser.parse(document.storage_path)
            text = TextCleaner.clean(text)
            language = LanguageDetector.detect(text)
            chunks = TextChunker().chunk(text)
            embedding_service = EmbeddingService()
            vector_store = FaissStore()
            metadata_store = MetadataStore()
            
            with DocumentProcessor._lock:
                metadata = metadata_store.load()
                
                for index, chunk in enumerate(chunks):
                    db.add(
                        DocumentChunk(
                            document_id=document.id,
                            chunk_index=index,
                            content=chunk,
                            token_count=len(chunk.split()),
                        )
                    )
                    vector = embedding_service.embed_text(chunk)
                    vector_store.add(vector.reshape(1, -1))
                    metadata.append({
                        "document_id": str(document.id),
                        "document_name": document.original_name,
                        "page": None,                 # We'll populate this for PDFs later
                        "chunk_index": index,
                        "content": chunk,
                        "language": language,
                        "tokens": len(chunk.split()),
                        "project_id": str(document.project_id) if document.project_id else None,
                    })

                metadata_store.save(metadata)
                
            document.language = language
            document.status = DocumentStatus.READY
            db.commit()
            
            # Reload global AI container to sync newly added chunks/embeddings
            import app.core.ai_container as container
            if container.ai_container is not None:
                container.ai_container.metadata = metadata
                container.ai_container.bm25.build(metadata)
                # Re-initialize FAISS store to load the updated index from disk
                container.ai_container.faiss = FaissStore()
                logger.info("Successfully reloaded global AI container with new document chunks.")

            logger.info(f"Successfully processed document {document_id}")
        except Exception as e:
            logger.exception(f"Error processing document {document_id}: {e}")
            try:
                document = db.query(Document).filter(Document.id == document_id).first()
                if document:
                    document.status = DocumentStatus.FAILED
                    db.commit()
            except Exception as inner_ex:
                logger.error(f"Failed to update document status to FAILED: {inner_ex}")
        finally:
            db.close()