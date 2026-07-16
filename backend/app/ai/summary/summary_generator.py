from app.ai.summary.summary_prompt import SUMMARY_PROMPT
from app.ai.llm.ollama_client import OllamaClient


class SummaryGenerator:

    def __init__(self):
        self.llm = OllamaClient()

    def generate(
        self,
        context: str,
    ) -> str:

        prompt = SUMMARY_PROMPT.format(
            context=context
        )

        return self.llm.generate(prompt)