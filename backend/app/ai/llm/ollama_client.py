from collections.abc import Generator
from ollama import Client
from app.ai.llm.models import (OLLAMA_MODEL,OLLAMA_URL,)

class OllamaClient:
    def __init__(self):
        self.client = Client(host=OLLAMA_URL)

    def generate(self, prompt: str) -> str:
        """
        Returns the complete response.
        """
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
        stream = self.client.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            stream=True,
        )

        for chunk in stream:
            yield chunk["response"]