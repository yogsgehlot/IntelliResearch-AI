from sentence_transformers import SentenceTransformer
from app.core.config import settings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

if settings.USE_NVIDIA and settings.NVIDIA_API_KEY:
    from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
    embedding_model = NVIDIAEmbeddings(
        model=settings.NVIDIA_EMBEDDING_MODEL,
        api_key=settings.NVIDIA_API_KEY,
        truncate="NONE",
    )
else:
    embedding_model = SentenceTransformer(MODEL_NAME)