from enum import Enum
from uuid import UUID
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ProcessingJob(BaseModel):
    __tablename__ = "processing_jobs"

    document_id: Mapped[UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    status: Mapped[JobStatus] = mapped_column(SqlEnum(JobStatus),default=JobStatus.PENDING,)
    error_message: Mapped[str | None] = mapped_column(String(1000),nullable=True,)
    document = relationship("Document",back_populates="jobs",)