from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.ai.llm.ollama_client import OllamaClient
from app.ai.rag.context_builder import ContextBuilder
from app.ai.report.markdown_formatter import MarkdownFormatter
from app.ai.reranker.reranker import Reranker
from app.ai.retrieval.retrieval_service import RetrievalService
from app.ai.summary.summary_prompt import SUMMARY_PROMPT

from app.models.research_summary import ResearchSummary

from app.repositories.project_repository import ProjectRepository
from app.repositories.research_summary_repository import (
    ResearchSummaryRepository,
)


class ResearchSummaryService:

    def __init__(self):
        self.retriever = RetrievalService()
        self.reranker = Reranker()
        self.llm = OllamaClient()

    def generate(
        self,
        db: Session,
        user,
        project_id: str,
        topic: str,
        summary_type: str = "project_summary",
    ):
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if project is None or project.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        # Retrieve relevant chunks
        chunks = self.retriever.retrieve(
            query=topic,
            project_id=str(project_id),
            top_k=20,
        )

        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No indexed documents found for this project.",
            )

        # Improve relevance
        chunks = self.reranker.rerank(
            topic,
            chunks,
        )

        # Build context
        context = ContextBuilder.build(chunks)

        # Generate prompt
        prompt = SUMMARY_PROMPT.format(
            topic=topic,
            summary_type=summary_type,
            context=context,
        )

        # Generate markdown summary
        content = MarkdownFormatter.clean(
            self.llm.generate(prompt)
        )

        # Check if summary already exists
        summary = ResearchSummaryRepository.get_by_project(
            db,
            project_id,
        )

        if summary is None:
            summary = ResearchSummary(
                project_id=project_id,
            )

        summary.topic = topic
        summary.summary_type = summary_type
        summary.content = content

        if getattr(summary, "id", None) is None:
            return ResearchSummaryRepository.create(
                db,
                summary,
            )

        return ResearchSummaryRepository.update(
            db,
            summary,
        )

    @staticmethod
    def list(
        db: Session,
        user,
        project_id: str,
    ):
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if project is None or project.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        summary = ResearchSummaryRepository.get_by_project(
            db,
            project_id,
        )

        if summary is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Summary not found",
            )

        return summary

    @staticmethod
    def delete(
        db: Session,
        user,
        project_id: str,
    ):
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if project is None or project.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        summary = ResearchSummaryRepository.get_by_project(
            db,
            project_id,
        )

        if summary is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Summary not found.",
            )

        ResearchSummaryRepository.delete(
            db,
            summary,
        )

        return {
            "message": "Summary deleted successfully."
        }