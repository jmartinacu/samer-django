from django.urls import path

from samer.questions import views

app_name = "questions"

urlpatterns = [
    path("", views.questions, name="questions"),
    path("create/", views.create, name="create"),
    path("archive/", views.archive, name="archive"),
    path(
        "create/answer/<str:question_id>/<str:edit>/",
        views.create_answer,
        name="create_answer",
    ),
    path("delete/<str:question_id>/", views.delete, name="delete"),
    path(
        "delete/root/<str:question_id>/",
        views.delete_root,
        name="delete_root",
    ),
    path(
        "like/<str:question_id>/",
        views.add_remove_like,
        name="add_remove_like",
    ),
]
