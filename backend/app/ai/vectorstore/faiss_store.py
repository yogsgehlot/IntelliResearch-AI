import faiss
import numpy as np
from pathlib import Path

class FaissStore:
    INDEX_PATH = Path("storage/faiss/index.bin")
    def __init__(self):
        self.dimension = 384
        if self.INDEX_PATH.exists():
            self.index = faiss.read_index(str(self.INDEX_PATH))

        else:
            self.index = faiss.IndexFlatIP(self.dimension)

    def add(self,vectors: np.ndarray,):
        self.index.add(vectors)
        self.save()

    def search(self,vector,top_k=5,):
        scores, ids = self.index.search(vector,top_k,)
        return scores, ids

    def save(self):
        self.INDEX_PATH.parent.mkdir(parents=True,exist_ok=True,)
        faiss.write_index(self.index,str(self.INDEX_PATH),)