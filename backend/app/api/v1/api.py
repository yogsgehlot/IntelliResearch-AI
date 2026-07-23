from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.documents import router as document_router
from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.projects import router as project_router
from app.api.v1.endpoints.reports import (router as report_router,)
from app.api.v1.endpoints.research_notes import (router as notes_router,)
from app.api.v1.endpoints.research_summary import (router as summary_router,)
from app.api.v1.endpoints.settings import router as settings_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(document_router)
api_router.include_router(chat_router)
api_router.include_router(project_router)

api_router.include_router(report_router,)

api_router.include_router(notes_router)
api_router.include_router(summary_router)
api_router.include_router(settings_router)