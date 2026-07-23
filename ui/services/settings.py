from services.api import api

class SettingsService:
    def get(self, token):
        return api.get(
            "/settings",
            token=token,
        )

    def update(self, token, data):
        return api.post(
            "/settings",
            token=token,
            data=data,
        )

settings_service = SettingsService()
