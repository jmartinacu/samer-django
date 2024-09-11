from django.urls import path

from samer.root import views

app_name = "root"

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
        "post/delete/<objectid:post_id>/",
        views.delete_post,
        name="delete_post",
    ),
    path(
        "user/delete/<objectid:user_id>/",
        views.delete_user,
        name="delete_user",
    ),
    path(
        "tag/delete/<objectid:tag_id>/",
        views.delete_tag,
        name="delete_tag",
    ),
    path("post/edit/<objectid:post_id>/", views.edit_post, name="edit_post"),
    path("post/<objectid:post_id>/", views.post_details, name="post_details"),
    path("user/<objectid:user_id>/", views.user_details, name="user_details"),
    path("tag/<objectid:tag_id>/", views.tag_details, name="tag_details"),
    path(
        "question/<objectid:question_id>/",
        views.question_details,
        name="question_details",
    ),
    path(
        "user/<objectid:user_id>/<objectid:question_id>/",
        views.remove_question,
        name="remove_question",
    ),
    path(
        "user/<objectid:user_id>/<objectid:post_id>/<objectid:comment_id>/",
        views.remove_comment,
        name="remove_comment",
    ),
]
