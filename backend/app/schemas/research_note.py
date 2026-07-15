from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class NoteCreate(BaseModel):

    project_id: UUID

    title: str

    content: str

    source_document: str | None = None


class NoteResponse(NoteCreate):

    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )