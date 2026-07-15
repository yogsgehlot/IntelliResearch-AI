from ollama import Client

from app.ai.llm.models import (
    OLLAMA_MODEL,
    OLLAMA_URL,
)

class OllamaClient:
    def __init__(self):
        self.client = Client(host=OLLAMA_URL,)

    def generate(self,prompt: str,) -> str:
        response = self.client.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            stream=False,
        )

        return response["response"]