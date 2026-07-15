import uuid

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Project(BaseModel):

    __tablename__ = "projects"

    id: Mapped[uuid.UUID]

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