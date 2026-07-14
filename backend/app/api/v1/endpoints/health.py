from fastapi import APIRouter
from app.core.config import settings
router = APIRouter()

@router.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
    }

@router.get("/version", tags=["Health"])
async def version():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.API_VERSION,
    }