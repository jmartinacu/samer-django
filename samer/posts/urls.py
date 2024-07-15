from django.urls import path

from samer.posts import views

app_name = 'posts'  # pylint: disable=C0103

urlpatterns = [
    path('like/<str:post_id>/', views.add_remove_like, name='add_remove_like'),
    path(
        'comment/remove/<str:post_id>/<str:comment_id>/',
        views.remove_comment,
        name='remove_comment'
    ),
    path(
        'comment/<str:post_id>/<str:post_type>',
        views.comments, name='comment'
    ),
]
