from uuid import UUID
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class DocumentChunk(BaseModel):
    __tablename__ = "document_chunks"

    document_id: Mapped[UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"),)
    chunk_index: Mapped[int] = mapped_column(Integer,nullable=False,)
    content: Mapped[str] = mapped_column(Text,nullable=False,)
    token_count: Mapped[int] = mapped_column(Integer,default=0,)
    document = relationship("Document",back_populates="chunks",)