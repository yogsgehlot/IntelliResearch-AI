from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.config import settings
from app.api.deps import get_current_user
import os

router = APIRouter(prefix="/settings", tags=["Settings"])

class SettingsUpdateSchema(BaseModel):
    use_nvidia: bool
    nvidia_api_key: str | None = None
    nvidia_llm_model: str = "meta/llama-3.1-70b-instruct"
    nvidia_embedding_model: str = "nvidia/llama-nemotron-embed-vl-1b-v2"

@router.get("")
def get_settings(current_user=Depends(get_current_user)):
    api_key_masked = None
    if settings.NVIDIA_API_KEY:
        api_key_masked = settings.NVIDIA_API_KEY[:6] + "..." + settings.NVIDIA_API_KEY[-4:] if len(settings.NVIDIA_API_KEY) > 10 else "..."
        
    return {
        "use_nvidia": settings.USE_NVIDIA,
        "nvidia_api_key": api_key_masked,
        "nvidia_llm_model": settings.NVIDIA_LLM_MODEL,
        "nvidia_embedding_model": settings.NVIDIA_EMBEDDING_MODEL,
    }

from sqlalchemy.orm import Session
from app.api.deps import get_db

@router.post("")
def update_settings(
    data: SettingsUpdateSchema,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings.USE_NVIDIA = data.use_nvidia
    if data.nvidia_api_key and not data.nvidia_api_key.endswith("..."):
        settings.NVIDIA_API_KEY = data.nvidia_api_key
    settings.NVIDIA_LLM_MODEL = data.nvidia_llm_model
    settings.NVIDIA_EMBEDDING_MODEL = data.nvidia_embedding_model
    
    # Save back to .env file
    env_path = ".env"
    if os.path.exists(env_path):
        lines = []
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        new_lines = []
        keys_updated = set()
        for line in lines:
            if "=" in line:
                key = line.split("=")[0].strip()
                if key == "USE_NVIDIA":
                    new_lines.append(f"USE_NVIDIA={settings.USE_NVIDIA}\n")
                    keys_updated.add(key)
                elif key == "NVIDIA_API_KEY" and settings.NVIDIA_API_KEY:
                    new_lines.append(f"NVIDIA_API_KEY={settings.NVIDIA_API_KEY}\n")
                    keys_updated.add(key)
                elif key == "NVIDIA_LLM_MODEL":
                    new_lines.append(f"NVIDIA_LLM_MODEL={settings.NVIDIA_LLM_MODEL}\n")
                    keys_updated.add(key)
                elif key == "NVIDIA_EMBEDDING_MODEL":
                    new_lines.append(f"NVIDIA_EMBEDDING_MODEL={settings.NVIDIA_EMBEDDING_MODEL}\n")
                    keys_updated.add(key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
                
        # Ensure the last line ends with a newline before appending new variables
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines[-1] = new_lines[-1] + "\n"
                
        if "USE_NVIDIA" not in keys_updated:
            new_lines.append(f"USE_NVIDIA={settings.USE_NVIDIA}\n")
        if "NVIDIA_API_KEY" not in keys_updated and settings.NVIDIA_API_KEY:
            new_lines.append(f"NVIDIA_API_KEY={settings.NVIDIA_API_KEY}\n")
        if "NVIDIA_LLM_MODEL" not in keys_updated:
            new_lines.append(f"NVIDIA_LLM_MODEL={settings.NVIDIA_LLM_MODEL}\n")
        if "NVIDIA_EMBEDDING_MODEL" not in keys_updated:
            new_lines.append(f"NVIDIA_EMBEDDING_MODEL={settings.NVIDIA_EMBEDDING_MODEL}\n")
            
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
    # Trigger model reload dynamically
    from app.ai.embedding.model import MODEL_NAME
    from sentence_transformers import SentenceTransformer
    if settings.USE_NVIDIA and settings.NVIDIA_API_KEY:
        from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
        import app.ai.embedding.model as emb_model
        emb_model.embedding_model = NVIDIAEmbeddings(
            model=settings.NVIDIA_EMBEDDING_MODEL,
            api_key=settings.NVIDIA_API_KEY,
            truncate="NONE",
        )
    else:
        import app.ai.embedding.model as emb_model
        emb_model.embedding_model = SentenceTransformer(MODEL_NAME)
        
    # Rebuild vector store dynamically to match new embedding model dimensions
    from app.services.document_service import DocumentService
    DocumentService.rebuild_vector_store(db)
        
    return {"message": "Settings updated and index rebuilt successfully"}
