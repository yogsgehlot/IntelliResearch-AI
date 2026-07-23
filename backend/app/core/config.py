from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_VERSION: str
    DEBUG: bool

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET: str
    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    USE_NVIDIA: bool = False
    NVIDIA_API_KEY: str | None = None
    NVIDIA_LLM_MODEL: str = "meta/llama-3.1-70b-instruct"
    NVIDIA_EMBEDDING_MODEL: str = "nvidia/llama-nemotron-embed-vl-1b-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()