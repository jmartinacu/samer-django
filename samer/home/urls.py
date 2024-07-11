from django.urls import path

from samer.home import views

app_name = 'home'  # pylint: disable=C0103

urlpatterns = [
    path('', views.home, name='home'),
]
