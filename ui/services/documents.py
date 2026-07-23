from services.api import api


class DocumentService:

    def upload(
        self,
        token,
        file,
    ):
        files = {
            "file": (
                file.name,
                file,
                file.type,
                )
            }

        return api.post(
            "/documents/upload",
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