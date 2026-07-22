import json
from pathlib import Path
import threading


class MetadataStore:

    FILE = Path("storage/faiss/metadata.json")
    _lock = threading.Lock()

    def load(self):
        with self._lock:
            if not self.FILE.exists():
                return []

            try:
                with open(self.FILE, "r", encoding="utf-8") as f:
                    if self.FILE.stat().st_size == 0:
                        return []

                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []

    def save(self, metadata):
        with self._lock:
            self.FILE.parent.mkdir(parents=True,exist_ok=True,)
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(metadata,f,indent=4,ensure_ascii=False,)