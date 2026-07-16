from uuid import UUID
from pydantic import BaseModel
from app.models.document import DocumentStatus

class DocumentResponse(BaseModel):
    id: UUID
    project_id: UUID | None = None
    original_name: str
    status: DocumentStatus
    file_size: int
    model_config = {
        "from_attributes": True
    }
