from enum import Enum
from uuid import UUID
from sqlalchemy import BigInteger, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"

class Document(BaseModel):
    __tablename__ = "documents"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False,)
    filename: Mapped[str] = mapped_column(String(255),nullable=False,)
    original_name: Mapped[str] = mapped_column(String(255),nullable=False,)
    mime_type: Mapped[str] = mapped_column(String(100),nullable=False,)
    extension: Mapped[str] = mapped_column(String(20),nullable=False,)
    file_size: Mapped[int] = mapped_column(BigInteger,nullable=False,)
    storage_path: Mapped[str] = mapped_column(String(500),nullable=False,)
    page_count: Mapped[int | None] = mapped_column(Integer,nullable=True,)
    language: Mapped[str | None] = mapped_column(String(20),nullable=True,)
    status: Mapped[DocumentStatus] = mapped_column(SqlEnum(DocumentStatus),default=DocumentStatus.UPLOADED,nullable=False,)

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    jobs = relationship(
        "ProcessingJob",
        back_populates="document",
        cascade="all, delete-orphan",
    )