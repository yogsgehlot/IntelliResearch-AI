from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ResearchSummaryGenerateRequest(BaseModel):
    topic: str
    summary_type: str = "project_summary"


class ResearchSummaryResponse(BaseModel):
    id: UUID
    project_id: UUID

    topic: str
    summary_type: str

    content: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True