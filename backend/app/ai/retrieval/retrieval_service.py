import app.core.ai_container as container


class RetrievalService:

    def retrieve(
        self,
        query: str,
        project_id: str,
        top_k: int = 20,
    ):

        if container.ai_container is None:
            raise RuntimeError(
                "AI Container not initialized."
            )

        # ---------- Dense Retrieval (FAISS) ----------

        vector = container.ai_container.embedding.embed_text(
            query
        )

        scores, ids = container.ai_container.faiss.search(
            vector.reshape(1, -1),
            top_k,
        )

        faiss_results = []

        for idx in ids[0]:

            if idx == -1:
                continue

            if idx >= len(container.ai_container.metadata):
                continue

            item = container.ai_container.metadata[idx]

            # Filter by Project
            if item["project_id"] != project_id:
                continue

            faiss_results.append(item)

        # ---------- Sparse Retrieval (BM25) ----------

        bm25 = container.ai_container.bm25.search(
            query,
            top_k * 2,
        )

        bm25_results = []

        for item in bm25:

            if item["project_id"] != project_id:
                continue

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

        return list(unique.values())