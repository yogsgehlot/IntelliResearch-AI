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


document_service = DocumentService()