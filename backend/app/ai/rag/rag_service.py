from app.ai.llm.ollama_client import OllamaClient
from app.ai.llm.prompt_builder import PromptBuilder

from app.ai.memory.query_rewriter import QueryRewriter

from app.ai.rag.context_builder import ContextBuilder
from app.ai.rag.citation_builder import CitationBuilder

from app.ai.retrieval.retrieval_service import RetrievalService
from app.ai.reranker.reranker import Reranker

from app.core.memory import memory


class RAGService:

    def __init__(self):
        self.retriever = RetrievalService()
        self.reranker = Reranker()
        self.llm = OllamaClient()
        self.rewriter = QueryRewriter()

    def ask(
        self,
        project_id: str,
        session_id: str,
        question: str,
    ):

        history_items = memory.history(session_id)

        history = "\n".join(
            f'{item["role"]}: {item["content"]}'
            for item in history_items
        )

        rewritten_question = self.rewriter.rewrite(
            question,
            history,
        )

        documents = self.retriever.retrieve(
            query=rewritten_question,
            project_id=project_id,
            top_k=20,
        )

        documents = self.reranker.rerank(
            rewritten_question,
            documents,
        )

        context = ContextBuilder.build(documents)

        prompt = PromptBuilder.build(
            question=rewritten_question,
            context=context,
            history=history,
        )

        answer = self.llm.generate(prompt)

        memory.add(
            session_id,
            "user",
            question,
        )

        memory.add(
            session_id,
            "assistant",
            answer,
        )

        citations = CitationBuilder.build(documents)

        return {
            "answer": answer,
            "sources": citations,
        }