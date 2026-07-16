from services.api import api


class AuthService:

    def login(
        self,
        email: str,
        password: str,
    ):

        response = api.post(
            "/auth/login",
            data={
                "email": email,
                "password": password,
            },
        )

        return response

    def register(
        self,
        name: str,
        email: str,
        password: str,
    ):

        return api.post(
            "/auth/register",
            data={
                "name": name,
                "email": email,
                "password": password,
            },
        )


auth_service = AuthService()