from collections.abc import Generator
from ollama import Client
from app.ai.llm.models import (OLLAMA_MODEL,OLLAMA_URL,)
from app.core.config import settings

class OllamaClient:
    def __init__(self):
        if not (settings.USE_NVIDIA and settings.NVIDIA_API_KEY):
            self.client = Client(host=OLLAMA_URL)
        else:
            self.client = None

    def generate(self, prompt: str) -> str:
        """
        Returns the complete response.
        """
        if settings.USE_NVIDIA and settings.NVIDIA_API_KEY:
            from langchain_nvidia_ai_endpoints import ChatNVIDIA
            llm = ChatNVIDIA(
                model=settings.NVIDIA_LLM_MODEL,
                api_key=settings.NVIDIA_API_KEY,
            )
            response = llm.invoke(prompt)
            return response.content
        else:
            response = self.client.generate(
                model=OLLAMA_MODEL,
                prompt=prompt,
                stream=False,
            )
            return response["response"]

    def stream(self, prompt: str) -> Generator[str, None, None]:
        """
        Streams the response token by token.
        """
        if settings.USE_NVIDIA and settings.NVIDIA_API_KEY:
            from langchain_nvidia_ai_endpoints import ChatNVIDIA
            llm = ChatNVIDIA(
                model=settings.NVIDIA_LLM_MODEL,
                api_key=settings.NVIDIA_API_KEY,
            )
            for chunk in llm.stream(prompt):
                yield chunk.content
        else:
            stream = self.client.generate(
                model=OLLAMA_MODEL,
                prompt=prompt,
                stream=True,
            )
            for chunk in stream:
                yield chunk["response"]