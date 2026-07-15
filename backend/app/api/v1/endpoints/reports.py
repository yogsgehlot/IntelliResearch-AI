from fastapi import APIRouter

from app.schemas.report import (
    ReportRequest,
    ReportResponse,
)

from app.services.report_service import (
    ReportService,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

service = ReportService()


@router.post(
    "/generate",
    response_model=ReportResponse,
)
def generate_report(
    request: ReportRequest,
):

    report = service.generate(

        request.project_id,

        request.topic,
    )

    return ReportResponse(
        report=report,
    )