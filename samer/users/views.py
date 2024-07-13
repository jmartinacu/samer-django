from django.shortcuts import render, redirect
from django.urls import reverse

from samer.users.models import User, user as user_mongo
from samer.users import hashing
from samer.users.context_processors import UserAuth
from samer.users.forms import LoginForm, SigninForm


def login(request):
    error_messages = []
    user_auth = UserAuth(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['pwd']
            try:
                user: User | None = user_mongo.find_one({'username': username})
            except Exception as e:  # pylint: disable=W0718
                error_messages.append(f"Ocurrió un error inesperado: {e}")
                return render(request, 'users/login.html', {
                    'errors': error_messages,
                    'login_form': form,
                })
            if user is None:
                error_messages.append(
                    'Nombre de usuario o contraseña incorrectos'
                )
                return render(request, 'users/login.html', {
                    'errors': error_messages,
                    'login_form': form,
                })
            if not hashing.check_password(password, user['password']):
                error_messages.append(
                    'Nombre de usuario o contraseña incorrectos'
                )
                return render(request, 'users/login.html', {
                    'errors': error_messages,
                    'login_form': form,
                })
            if user['admin']:
                user_auth.login(
                    username=username, id=str(user['_id']),
                    email=user['email'], admin=True
                )
            else:
                user_auth.login(username=username, id=str(user['_id']))
            return redirect(reverse('home:home_images'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {
        'errors': error_messages,
        'login_form': form,
    })


def signin(request):
    error_messages = []
    user_auth = UserAuth(request)
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['pwd']
            hashed_pwd = hashing.hash_password(password)
            try:
                users = user_mongo.find(query={'username': username})
                if len(list(users)) > 0:
                    error_messages.append('Nombre de usuario ya usado')
                    return render(request, 'users/signin.html', {
                        'errors': error_messages,
                        'signin_form': form,
                    })
                res_user = user_mongo.create(
                    username=username, password=hashed_pwd
                )
                user_auth.login(
                    username=username, id=str(res_user.inserted_id)
                )
                return redirect(reverse('home:home_images'))
            except Exception as e:  # pylint: disable=W0718
                error_messages.append(f"Ocurrió un error inesperado: {e}")
                return render(request, 'users/signin.html', {
                    'errors': error_messages,
                    'signin_form': form,
                })
    else:
        form = SigninForm()
    return render(request, 'users/signin.html', {
        'errors': error_messages,
        'signin_form': form,
    })


def logout(request):
    user_auth = UserAuth(request)
    user_auth.logout()
    return redirect(reverse('home:home_images'))
