from sqlalchemy.orm import Session
from app.ai.chunking.chunker import TextChunker
from app.ai.parser.parser_factory import ParserFactory
from app.ai.preprocessing.cleaner import TextCleaner
from app.ai.preprocessing.language import LanguageDetector
from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.ai.embedding.embedding_service import EmbeddingService
from app.ai.vectorstore.faiss_store import FaissStore
from app.ai.vectorstore.metadata_store import MetadataStore


class DocumentProcessor:

    @staticmethod
    def process(db: Session,document: Document,) -> Document:
        parser = ParserFactory.get_parser(document.extension)
        text = parser.parse(document.storage_path)
        text = TextCleaner.clean(text)
        language = LanguageDetector.detect(text)
        chunks = TextChunker().chunk(text)
        embedding_service = EmbeddingService()
        vector_store = FaissStore()
        metadata_store = MetadataStore()
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
                "chunk_index": index,
                "content": chunk,
            })

        metadata_store.save(metadata)
        document.language = language
        document.status = DocumentStatus.READY
        db.commit()
        db.refresh(document)
        return document