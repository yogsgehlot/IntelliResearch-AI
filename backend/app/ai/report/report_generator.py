from app.ai.llm.ollama_client import OllamaClient
from app.ai.report.report_prompt import REPORT_TEMPLATE


class ReportGenerator:
    def __init__(self):
        self.llm = OllamaClient()

    def generate(self,topic: str,context: str,):
        prompt = REPORT_TEMPLATE.format(topic=topic,context=context,)

        return self.llm.generate(prompt)