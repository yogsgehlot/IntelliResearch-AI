from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID
class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)