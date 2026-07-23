from pathlib import Path
import shutil

from app.storage.base import BaseStorage

class LocalStorage(BaseStorage):

    ROOT = Path(__file__).resolve().parents[2] / "storage" / "original"

    def save(self, file, filename: str):
        extension = filename.split(".")[-1].lower()
        folder = self.ROOT / extension
        folder.mkdir(parents=True,exist_ok=True,)
        path = folder / filename
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return str(path)

    def delete(self, path: str):
        Path(path).unlink(missing_ok=True)