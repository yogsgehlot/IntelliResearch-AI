from services.api import api


class ChatService:

    def ask(
        self,
        token,
        # project_id,
        question,
    ):
        print(api.post("/chat",token=token,data={"question": question,},))
        return api.post(
            "/chat",
            token=token,
            data={
                # "project_id": project_id,
                "question": question,
            },
        )


chat_service = ChatService()