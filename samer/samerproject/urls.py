from django.urls import path, include


urlpatterns = [
    path("", include("home.urls", namespace="home")),
    path("users/", include("users.urls", namespace="users")),
    path("posts/", include("posts.urls", namespace="posts")),
    path("questions/", include("questions.urls", namespace="questions")),
    path("root/", include("root.urls", namespace="root")),
]
