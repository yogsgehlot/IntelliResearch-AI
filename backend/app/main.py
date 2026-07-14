from fastapi import FastAPI
from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)

app.include_router(
    api_router,
    prefix="/api/v1",
)

logger.info("Application Started")

@app.get("/")
async def root():
    return {
        "message": "Welcome to IntelliResearch AI"
    }