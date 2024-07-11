from django.urls import path

from samer.root import views

app_name = 'root'  # pylint: disable=C0103

urlpatterns = [
    path('', views.root, name='root'),
    path('upload/', views.upload_image_post, name='upload'),
]
