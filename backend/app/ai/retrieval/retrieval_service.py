import app.core.ai_container as container


class RetrievalService:

    def retrieve(
        self,
        query: str,
        # project_id: str,
        document_id: str = None,
        top_k: int = 20,
    ):

        if container.ai_container is None:
            raise RuntimeError(
                "AI Container not initialized."
            )

        # If filtering by a single document, increase search depth to find matches
        search_k = 1000 if document_id else top_k

        # ---------- Dense Retrieval (FAISS) ----------

        vector = container.ai_container.embedding.embed_text(
            query
        )

        scores, ids = container.ai_container.faiss.search(
            vector.reshape(1, -1),
            search_k,
        )

        faiss_results = []

        for idx in ids[0]:

            if idx == -1:
                continue

            if idx >= len(container.ai_container.metadata):
                continue

            item = container.ai_container.metadata[idx]

            # Filter by Document
            if document_id and item.get("document_id") != str(document_id):
                continue

            # Filter by Project
            # if item["project_id"] != project_id:
            #     continue

            faiss_results.append(item)

        # ---------- Sparse Retrieval (BM25) ----------

        bm25 = container.ai_container.bm25.search(
            query,
            search_k * 2,
        )

        bm25_results = []

        for item in bm25:

            # Filter by Document
            if document_id and item.get("document_id") != str(document_id):
                continue

            # if item["project_id"] != project_id:
            #     continue

            bm25_results.append(item)

        # ---------- Merge Results ----------

        merged = faiss_results + bm25_results

        unique = {}

        for item in merged:

            key = (
                item["document_id"],
                item["chunk_index"],
            )

            unique[key] = item

        return list(unique.values())[:top_k]