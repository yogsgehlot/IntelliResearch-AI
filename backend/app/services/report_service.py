from app.ai.rag.context_builder import ContextBuilder
from app.ai.report.markdown_formatter import MarkdownFormatter
from app.ai.report.report_generator import ReportGenerator
from app.ai.retrieval.retrieval_service import RetrievalService


class ReportService:

    def __init__(self):

        self.retriever = RetrievalService()

        self.context_builder = ContextBuilder()

        self.generator = ReportGenerator()

    def generate(
        self,
        project_id: str,
        topic: str,
    ):

        chunks = self.retriever.retrieve(

            query=topic,

            project_id=project_id,

            top_k=20,
        )

        context = self.context_builder.build(
            chunks,
        )

        report = ""

        for chunk in self.generator.generate(
            topic,
            context,
        ):

            report += chunk

        report = MarkdownFormatter.clean(
            report,
        )

        return report