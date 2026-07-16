from sqlalchemy.orm import Session

from app.models.citation import Citation
from app.repositories.citation_repository import CitationRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.citation import CitationCreate


class CitationService:
    @staticmethod
    def _authors(authors: str | None) -> str:
        return authors.strip() if authors else "Unknown Author"

    @staticmethod
    def _year(year: str | None) -> str:
        return year.strip() if year else "n.d."

    @staticmethod
    def _slug(title: str) -> str:
        words = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in title)
        parts = [part.lower() for part in words.split()[:4]]
        return "_".join(parts) or "citation"

    @classmethod
    def build_formats(cls, data: CitationCreate):
        authors = cls._authors(data.authors)
        year = cls._year(data.year)
        title = data.title.strip()
        source = data.source.strip() if data.source else "Uploaded document"
        doi = f" https://doi.org/{data.doi.strip()}" if data.doi else ""
        url = f" {data.url.strip()}" if data.url else ""
        key = f"{cls._slug(title)}_{year}".replace(".", "")

        apa = f"{authors}. ({year}). {title}. {source}.{doi or url}"
        mla = f'{authors}. "{title}." {source}, {year}.{doi or url}'
        ieee = f'{authors}, "{title}," {source}, {year}.{doi or url}'
        bibtex = (
            f"@misc{{{key},\n"
            f"  author = {{{authors}}},\n"
            f"  title = {{{title}}},\n"
            f"  year = {{{year}}},\n"
            f"  howpublished = {{{source}}},\n"
            f"  doi = {{{data.doi or ''}}},\n"
            f"  url = {{{data.url or ''}}}\n"
            f"}}"
        )

        return apa.strip(), mla.strip(), ieee.strip(), bibtex

    @classmethod
    def create(cls, db: Session, user, data: CitationCreate):
        project = ProjectRepository.get_by_id(db, data.project_id)

        if project is None or project.owner_id != user.id:
            raise ValueError("Project not found")

        apa, mla, ieee, bibtex = cls.build_formats(data)

        citation = Citation(
            project_id=data.project_id,
            document_id=data.document_id,
            title=data.title,
            authors=data.authors,
            year=data.year,
            source=data.source,
            doi=data.doi,
            url=data.url,
            apa=apa,
            mla=mla,
            ieee=ieee,
            bibtex=bibtex,
        )

        return CitationRepository.create(db, citation)

    @staticmethod
    def list(db: Session, user, project_id: str):
        project = ProjectRepository.get_by_id(db, project_id)

        if project is None or project.owner_id != user.id:
            raise ValueError("Project not found")

        return CitationRepository.get_by_project(db, project_id)
