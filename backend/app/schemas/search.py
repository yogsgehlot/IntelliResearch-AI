from pydantic import BaseModel


class SearchRequest(BaseModel):
    project_id: str
    query: str
    top_k: int = 10


class SearchResult(BaseModel):
    project_id: str | None = None
    document_id: str
    document_name: str | None = None
    page: int | None = None
    chunk_index: int
    content: str


class SearchResponse(BaseModel):
    results: list[SearchResult]
