from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, UserResponse
from app.schemas.token import TokenResponse
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import CurrentUserResponse

router = APIRouter(prefix="/auth",tags=["Authentication"],)

@router.post("/register",response_model=UserResponse,)
def register(request: RegisterRequest,db: Session = Depends(get_db),):
    try:
        return AuthService.register(db,request,)

    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e),)

@router.post("/login",response_model=TokenResponse, )
def login(request: LoginRequest,db: Session = Depends(get_db),):
    try:
        return AuthService.login(db,request,)

    except ValueError as e:
        raise HTTPException(status_code=401,detail=str(e),)
    
@router.get("/me",response_model=CurrentUserResponse,)
def me(current_user: User = Depends(get_current_user),):
    return current_user