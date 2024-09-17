from django.urls import path

from samer.home import views

app_name = "home"

urlpatterns = [
    path("", views.home_images, name="home_images"),
    path("videos/", views.home_videos, name="home_videos"),
    path("edit/", views.home_edit_profile, name="home_edit_profile"),
    path("messages/", views.add_message, name="home_message"),
    path("tag/<objectid:tag_id>/", views.home_tag, name="home_tag"),
]
