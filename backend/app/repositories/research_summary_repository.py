from sqlalchemy.orm import Session

from app.models.research_summary import ResearchSummary


class ResearchSummaryRepository:

    @staticmethod
    def get_by_project(
        db: Session,
        project_id,
    ):
        return (
            db.query(ResearchSummary)
            .filter(ResearchSummary.project_id == project_id)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        summary: ResearchSummary,
    ):
        db.add(summary)

        db.commit()

        db.refresh(summary)

        return summary

    @staticmethod
    def update(
        db: Session,
        summary: ResearchSummary,
    ):
        db.commit()

        db.refresh(summary)

        return summary

    @staticmethod
    def delete(
        db: Session,
        summary: ResearchSummary,
    ):
        db.delete(summary)

        db.commit()