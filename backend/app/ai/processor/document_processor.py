from sqlalchemy.orm import Session
from app.ai.chunking.chunker import TextChunker
from app.ai.parser.parser_factory import ParserFactory
from app.ai.preprocessing.cleaner import TextCleaner
from app.ai.preprocessing.language import LanguageDetector
from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk


class DocumentProcessor:

    @staticmethod
    def process(db: Session,document: Document,) -> Document:
        parser = ParserFactory.get_parser(document.extension)
        text = parser.parse(document.storage_path)
        text = TextCleaner.clean(text)
        language = LanguageDetector.detect(text)
        chunks = TextChunker().chunk(text)

        for index, chunk in enumerate(chunks):
            db.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                    token_count=len(chunk.split()),
                )
            )

        document.language = language
        document.status = DocumentStatus.READY
        db.commit()
        db.refresh(document)
        return document