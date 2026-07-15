from sqlalchemy.orm import Session

from app.models.research_note import ResearchNote

from app.repositories.research_note_repository import (
    ResearchNoteRepository,
)


class ResearchNoteService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):

        note = ResearchNote(**data.model_dump())

        return ResearchNoteRepository.create(
            db,
            note,
        )

    @staticmethod
    def list(
        db: Session,
        project_id,
    ):

        return ResearchNoteRepository.get_by_project(
            db,
            project_id,
        )