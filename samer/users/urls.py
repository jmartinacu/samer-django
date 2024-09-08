from django.urls import path

from samer.users import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),
]
