from django.conf import settings


class UserAuth:
    def __init__(self, request):
        self.session = request.session
        user_auth = self.session.get(settings.AUTHUSER_SESSION_ID)
        if not user_auth:
            user_auth = self.session[settings.AUTHUSER_SESSION_ID] = {}
        self.user_auth = user_auth

    def save(self):
        self.session.modified = True

    def login(
        self,
        username: str,
        id: str,
        email: str = "",
        admin: bool = False,
    ):
        self.user_auth["username"] = username
        self.user_auth["id"] = id
        self.user_auth["email"] = email
        self.user_auth["admin"] = admin
        self.save()

    def logout(self):
        self.user_auth = self.session[settings.AUTHUSER_SESSION_ID] = {}
        self.save()

    def is_login(self):
        return "username" in self.user_auth

    def is_admin(self):
        return "admin" in self.user_auth and self.user_auth["admin"]


def user_auth(request):
    return {"user_auth": UserAuth(request)}
