from sqlalchemy.orm import Session

from app.models.citation import Citation


class CitationRepository:
    @staticmethod
    def create(db: Session, citation: Citation):
        db.add(citation)
        db.commit()
        db.refresh(citation)
        return citation

    @staticmethod
    def get_by_project(db: Session, project_id):
        return (
            db.query(Citation)
            .filter(Citation.project_id == project_id)
            .order_by(Citation.created_at.desc())
            .all()
        )
