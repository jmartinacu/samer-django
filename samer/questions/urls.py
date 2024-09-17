from django.urls import path

from samer.questions import views

app_name = "questions"

urlpatterns = [
    path("", views.questions, name="questions"),
    path("create/", views.create, name="create"),
    path("archive/", views.archive, name="archive"),
    path("<objectid:question_id>/", views.question, name="question"),
    path(
        "create/answer/<objectid:question_id>/<str:edit>/",
        views.create_answer,
        name="create_answer",
    ),
    path("delete/<objectid:question_id>/", views.delete, name="delete"),
    path(
        "delete/root/<objectid:question_id>/",
        views.delete_root,
        name="delete_root",
    ),
    path(
        "like/<objectid:question_id>/",
        views.add_remove_like,
        name="add_remove_like",
    ),
]
