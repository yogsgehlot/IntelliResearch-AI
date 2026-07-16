from services.api import api


class ProjectService:

    def list(self, token):

        return api.get(
            "/projects",
            token=token,
        )

    def create(
        self,
        token,
        name,
        description,
    ):

        return api.post(
            "/projects",
            token=token,
            data={
                "name": name,
                "description": description,
            },
        )


project_service = ProjectService()