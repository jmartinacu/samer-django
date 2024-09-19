from django.urls import path

from samer.posts import views

app_name = "posts"

urlpatterns = [
    path("test/comment/", views.test_detoxify_comments, name="test_comments"),
    path(
        "like/<objectid:post_id>/",
        views.add_remove_like,
        name="add_remove_like",
    ),
    path("search/", views.search_posts, name="search_posts"),
    path(
        "tag/add/<objectid:tag_id>/",
        views.add_post_to_tag,
        name="add_posts_tag",
    ),
    path(
        "comment/remove/<objectid:post_id>/<objectid:comment_id>/",
        views.remove_comment,
        name="remove_comment",
    ),
    path(
        "comment/<objectid:post_id>/<str:post_type>/",
        views.comments,
        name="comment",
    ),
]
