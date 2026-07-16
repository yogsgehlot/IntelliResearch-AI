import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
# define/import UUID 



class Project(BaseModel):

    __tablename__ = "projects"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="projects",
    )

    documents = relationship(
        "Document",
        back_populates="project",
        cascade="all, delete",
    )
    
    notes = relationship(
        "ResearchNote",
        back_populates="project",
        cascade="all, delete",
    )

    summaries = relationship(
        "ResearchSummary",
        back_populates="project",
        cascade="all, delete",
    )

    citations = relationship(
        "Citation",
        back_populates="project",
        cascade="all, delete",
    )

    summary = relationship(
        "ResearchSummary",
        uselist=False,
        cascade="all, delete-orphan",
        back_populates="project",
    )