from services.api import api

class SummaryService:
    def get(self, token, project_id):
        return api.get(
            f"/projects/{project_id}/summary",
            token=token,
        )

    def generate(self, token, project_id, topic, summary_type="project_summary"):
        return api.post(
            f"/projects/{project_id}/summary",
            token=token,
            data={
                "topic": topic,
                "summary_type": summary_type,
            },
        )

    def delete(self, token, project_id):
        return api.delete(
            f"/projects/{project_id}/summary",
            token=token,
        )

summary_service = SummaryService()
