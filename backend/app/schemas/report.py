from pydantic import BaseModel


class ReportRequest(BaseModel):

    project_id: str

    topic: str


class ReportResponse(BaseModel):

    report: str