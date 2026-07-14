from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.user import UserRole

class CurrentUserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    model_config = ConfigDict(
        from_attributes=True
    )