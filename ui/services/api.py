import requests

from config import API_BASE_URL


class APIClient:

    def __init__(self):
        self.base_url = API_BASE_URL

    def get(
        self,
        endpoint,
        token=None,
    ):

        headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return requests.get(
            self.base_url + endpoint,
            headers=headers,
        )

    def post(
        self,
        endpoint,
        data=None,
        files=None,
        token=None,
    ):

        headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        url = self.base_url + endpoint

        # Multipart upload
        if files:
            return requests.post(
                url,
                data=data,
                files=files,
                headers=headers,
            )

        # JSON request
        return requests.post(
            url,
            json=data,
            headers=headers,
        )


api = APIClient()