from app.ai.retrieval.retrieval_service import RetrievalService


class SearchService:
    def __init__(self):
        self.retriever = RetrievalService()

    def search(self, project_id: str, query: str, top_k: int = 10):
        results = self.retriever.retrieve(
            query=query,
            project_id=project_id,
            top_k=top_k,
        )

        return results[:top_k]
