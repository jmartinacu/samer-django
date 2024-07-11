from django.urls import path

from samer.users import views

app_name = 'users'  # pylint: disable=C0103

urlpatterns = [
    path('login/', views.login, name='login'),
    path('sigin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
]
