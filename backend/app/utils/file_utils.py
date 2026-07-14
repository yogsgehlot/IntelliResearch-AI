import uuid
from pathlib import Path

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt",
    "png",
    "jpg",
    "jpeg",
}

def validate_extension(filename: str):
    extension = Path(filename).suffix.lower().replace(".", "")
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file")
    return extension

def generate_filename(filename: str):
    extension = Path(filename).suffix
    return f"{uuid.uuid4()}{extension}"