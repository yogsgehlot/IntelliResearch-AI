import faiss
import numpy as np
from pathlib import Path
import threading

class FaissStore:
    INDEX_PATH = Path("storage/faiss/index.bin")
    _lock = threading.Lock()

    def __init__(self):
        self.dimension = 384
        with self._lock:
            if self.INDEX_PATH.exists():
                self.index = faiss.read_index(str(self.INDEX_PATH))
            else:
                self.index = faiss.IndexFlatIP(self.dimension)

    def add(self, vectors: np.ndarray):
        with self._lock:
            self.index.add(vectors)
            self.save_unlocked()

    def search(self, vector, top_k=5):
        with self._lock:
            scores, ids = self.index.search(vector, top_k)
            return scores, ids

    def save_unlocked(self):
        self.INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.INDEX_PATH))

    def save(self):
        with self._lock:
            self.save_unlocked()