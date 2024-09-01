from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

from samer.users.context_processors import UserAuth


def get_path(path_info):
    result = ""
    if path_info["type"] == "static":
        result = reverse(path_info["name"])
    if path_info["type"] == "dynamic":
        result = reverse(
            path_info["name"],
            args=path_info["args"],
        ).rstrip("/")
        result = result.rsplit("/", len(path_info["args"]))
        result = result[0] + "/"
    return result


class RootMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        include_paths = [get_path(p) for p in settings.AUTH_INCLUDE_PATHS]
        include_paths.append("/root/")
        if any(request.path.startswith(path) for path in include_paths):
            user_auth = UserAuth(request)
            if not user_auth.is_admin():
                return redirect(reverse("users:login"))
        response = self.get_response(request)
        return response
