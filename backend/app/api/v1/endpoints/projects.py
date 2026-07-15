from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db

from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
)

from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return ProjectService.create(
        db,
        user,
        data,
    )


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return ProjectService.list(
        db,
        user,
    )