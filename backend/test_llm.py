from app.ai.llm.ollama_client import OllamaClient

client = OllamaClient()

response = client.generate(
    "What is Machine Learning?"
)

print(response)