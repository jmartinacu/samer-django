from django.urls import path

from samer.posts import views

app_name = 'posts'  # pylint: disable=C0103

urlpatterns = [
    path('like/<str:post_id>/', views.add_remove_like, name='add_remove_like'),
    path('comment/<str:post_id>/', views.comments, name='comments'),
]
