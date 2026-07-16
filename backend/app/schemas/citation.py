from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CitationCreate(BaseModel):
    project_id: UUID
    document_id: UUID | None = None
    title: str
    authors: str | None = None
    year: str | None = None
    source: str | None = None
    doi: str | None = None
    url: str | None = None


class CitationResponse(CitationCreate):
    id: UUID
    apa: str
    mla: str
    ieee: str
    bibtex: str

    model_config = ConfigDict(from_attributes=True)
