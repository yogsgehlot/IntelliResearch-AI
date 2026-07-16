from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import BaseModel


class Citation(BaseModel):
    __tablename__ = "citations"

    project_id = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    document_id = mapped_column(
        ForeignKey("documents.id"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    authors: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    year: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    source: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    doi: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    apa: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    mla: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    ieee: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    bibtex: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    project = relationship(
        "Project",
        back_populates="citations",
    )
