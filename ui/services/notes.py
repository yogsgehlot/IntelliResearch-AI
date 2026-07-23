from services.api import api


class NotesService:

    def list(
        self,
        token,
        project_id,
    ):
        return api.get(
            f"/notes/{project_id}",
            token=token,
        )

    def create(
        self,
        token,
        project_id,
        title,
        content,
    ):
        return api.post(
            "/notes",
            token=token,
            data={
                "project_id": project_id,
                "title": title,
                "content": content,
            },
        )


notes_service = NotesService()