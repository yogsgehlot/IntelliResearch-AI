from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.api.deps import get_current_user

from app.schemas.research_summary import (
    ResearchSummaryGenerateRequest,
    ResearchSummaryResponse,
)

from app.services.research_summary_service import (
    ResearchSummaryService,
)

router = APIRouter(
    prefix="/projects",
    tags=["Research Summary"],
)

service = ResearchSummaryService()


@router.post(
    "/{project_id}/summary",
    response_model=ResearchSummaryResponse,
)
def generate_summary(
    project_id: UUID,
    body: ResearchSummaryGenerateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return service.generate(
        db=db,
        user=user,
        project_id=project_id,
        topic=body.topic,
        summary_type=body.summary_type,
    )


@router.get(
    "/{project_id}/summary",
    response_model=ResearchSummaryResponse,
)
def get_summary(
    project_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return service.list(
        db,
        user,
        project_id,
    )


@router.delete(
    "/{project_id}/summary",
)
def delete_summary(
    project_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return service.delete(
        db,
        user,
        project_id,
    )