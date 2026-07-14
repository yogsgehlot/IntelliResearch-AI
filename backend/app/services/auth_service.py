from sqlalchemy.orm import Session
from app.core.security import (create_access_token,create_refresh_token,hash_password,verify_password,)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.token import TokenResponse
class AuthService:

    @staticmethod
    def register(db: Session,request: RegisterRequest,):
        existing = UserRepository.get_by_email(db,request.email,)

        if existing:
            raise ValueError("Email already registered")

        user = User(
            full_name=request.full_name,
            email=request.email,
            password_hash=hash_password(request.password),
        )

        return UserRepository.create(db,user,)

    @staticmethod
    def login(db: Session,request: LoginRequest,):
        user = UserRepository.get_by_email(db,request.email,)

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(request.password,user.password_hash,):
            raise ValueError("Invalid credentials")

        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )