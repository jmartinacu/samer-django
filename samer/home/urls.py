from django.urls import path

from samer.home import views

app_name = 'home'  # pylint: disable=C0103

urlpatterns = [
    path('', views.home_images, name='home_images'),
    path('videos/', views.home_videos, name='home_videos'),
    path('edit/', views.home_edit_profile, name='home_edit_profile'),
]
