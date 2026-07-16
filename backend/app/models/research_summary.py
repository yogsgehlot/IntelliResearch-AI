from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base
import uuid

from sqlalchemy.dialects.postgresql import UUID

class ResearchSummary(Base):
    __tablename__ = "research_summaries"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    executive_summary = Column(Text, nullable=False)

    research_objective = Column(Text)

    methodology = Column(Text)

    key_findings = Column(Text)

    limitations = Column(Text)

    future_work = Column(Text)

    keywords = Column(Text)

    conclusion = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    project = relationship(
        "Project",
        back_populates="summary",
    )