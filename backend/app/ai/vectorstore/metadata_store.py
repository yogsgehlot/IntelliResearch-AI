import json
from pathlib import Path

class MetadataStore:
    FILE = Path("storage/faiss/metadata.json")
    def load(self):
        if not self.FILE.exists():
            return []

        with open(self.FILE) as f:
            return json.load(f)

    def save(self, metadata):
        self.FILE.parent.mkdir(parents=True,exist_ok=True,)
        with open(self.FILE,"w",) as f:
            json.dump(metadata,f,indent=4,)