from services.api import api


class DocumentService:

    def upload(
        self,
        token,
        file,
        project_id=None,
    ):
        files = {
            "file": (
                file.name,
                file,
                file.type,
                )
            }

        url = "/documents/upload"
        if project_id:
            url += f"?project_id={project_id}"

        return api.post(
            url,
            token=token,
            files=files,
        )

    def list(self, token):
        return api.get(
            "/documents",
            token=token,
        )

    def delete(self, token, document_id):
        return api.delete(
            f"/documents/{document_id}",
            token=token,
        )


document_service = DocumentService()