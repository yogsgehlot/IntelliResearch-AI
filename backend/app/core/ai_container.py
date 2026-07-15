from app.ai.bm25.bm25_store import BM25Store
from app.ai.embedding.embedding_service import EmbeddingService
from app.ai.vectorstore.faiss_store import FaissStore
from app.ai.vectorstore.metadata_store import MetadataStore


class AIContainer:

    def __init__(self):

        print("Loading AI Components...")

        self.embedding = EmbeddingService()

        self.faiss = FaissStore()

        self.metadata_store = MetadataStore()

        self.metadata = self.metadata_store.load()

        self.bm25 = BM25Store()

        self.bm25.build(self.metadata)

        print("AI Components Ready")


ai_container: AIContainer | None = None