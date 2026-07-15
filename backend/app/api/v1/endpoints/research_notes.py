from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schemas.research_note import (
    NoteCreate,
    NoteResponse,
)

from app.services.research_note_service import (
    ResearchNoteService,
)

router = APIRouter(
    prefix="/notes",
    tags=["Research Notes"],
)


@router.post(
    "",
    response_model=NoteResponse,
)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
):

    return ResearchNoteService.create(
        db,
        note,
    )


@router.get(
    "/{project_id}",
    response_model=list[NoteResponse],
)
def list_notes(
    project_id: str,
    db: Session = Depends(get_db),
):

    return ResearchNoteService.list(
        db,
        project_id,
    )