from sqlalchemy.orm import Session

from app.models.research_note import ResearchNote


class ResearchNoteRepository:

    @staticmethod
    def create(
        db: Session,
        note: ResearchNote,
    ):

        db.add(note)
        db.commit()
        db.refresh(note)

        return note

    @staticmethod
    def get_by_project(
        db: Session,
        project_id,
    ):

        return (
            db.query(ResearchNote)
            .filter(
                ResearchNote.project_id == project_id
            )
            .all()
        )