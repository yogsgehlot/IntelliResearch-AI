from services.api import api


class ChatService:

    def ask(
        self,
        token,
        question,
        document_id=None,
    ):
        data = {
            "question": question,
        }
        if document_id:
            data["document_id"] = str(document_id)
            
        return api.post(
            "/chat",
            token=token,
            data=data,
        )


chat_service = ChatService()