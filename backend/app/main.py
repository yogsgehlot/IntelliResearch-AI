from contextlib import asynccontextmanager
import nltk
from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logger import logger
from app.core.startup import initialize_ai

# Download only once during development
nltk.download("punkt")
nltk.download("punkt_tab")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AI Components...")
    initialize_ai()
    logger.info("AI Components Ready")

    yield

    logger.info("Application Shutdown")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.include_router(api_router,prefix="/api/v1",)

@app.get("/")
async def root():
    return {
        "message": "Welcome to IntelliResearch AI"
    }

logger.info("Application Started")