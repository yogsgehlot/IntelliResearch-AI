from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.project_repository import ProjectRepository


class ProjectService:

    @staticmethod
    def create(
        db: Session,
        user,
        data,
    ):

        project = Project(

            name=data.name,

            description=data.description,

            owner_id=user.id,
        )

        return ProjectRepository.create(
            db,
            project,
        )

    @staticmethod
    def list(
        db: Session,
        user,
    ):

        return ProjectRepository.get_all(
            db,
            user.id,
        )