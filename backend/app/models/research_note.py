from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class ResearchNote(BaseModel):

    __tablename__ = "research_notes"

    project_id = Column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    source_document = Column(
        String(255),
    )

    project = relationship(
        "Project",
        back_populates="notes",
    )