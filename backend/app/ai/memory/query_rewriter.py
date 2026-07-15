from app.ai.llm.ollama_client import OllamaClient


class QueryRewriter:

    def __init__(self):
        self.llm = OllamaClient()

    def rewrite(
        self,
        question: str,
        history: str,
    ):

        if not history:
            return question

        prompt = f"""
Conversation History:

{history}

Rewrite the latest user question into a standalone question.

Question:
{question}

Standalone Question:
"""

        return self.llm.generate(prompt)