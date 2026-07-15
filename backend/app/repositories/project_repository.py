from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:

    @staticmethod
    def create(
        db: Session,
        project: Project,
    ):

        db.add(project)

        db.commit()

        db.refresh(project)

        return project

    @staticmethod
    def get_all(
        db: Session,
        owner_id,
    ):

        return (
            db.query(Project)
            .filter(Project.owner_id == owner_id)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        project_id,
    ):

        return (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )