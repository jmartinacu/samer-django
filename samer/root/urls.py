from django.urls import path

from samer.root import views

app_name = "root"  # pylint: disable=C0103

urlpatterns = [
    path("", views.root, name="root"),
    path("users/", views.users, name="users"),
    path("tags/", views.tags, name="tags"),
    path("questions/", views.questions, name="questions"),
    path("users/admin/", views.create_admin, name="create_admin"),
    path("post/upload/", views.upload_post, name="upload_post"),
    path(
        "actions/tag/",
        views.tag_action,
        name="tag_action",
    ),
    path(
        "actions/delete/<str:model>/",
        views.delete_action,
        name="delete_action",
    ),
    path(
        "post/delete/<str:post_id>/",
        views.delete_post,
        name="delete_post",
    ),
    path(
        "tag/delete/<str:tag_id>/",
        views.delete_tag,
        name="delete_tag",
    ),
    path("post/edit/<str:post_id>/", views.edit_post, name="edit_post"),
    path("post/<str:post_id>/", views.post_details, name="post_details"),
    path("user/<str:user_id>/", views.user_details, name="user_details"),
    path("tag/<str:tag_id>/", views.tag_details, name="tag_details"),
    path(
        "question/<str:question_id>/",
        views.question_details,
        name="question_details",
    ),
]
