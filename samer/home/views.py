from django.shortcuts import render, redirect
from django.urls import reverse

from samer.utils import upload_file, delete_file
from samer.home.models import profile as mongo_profile
from samer.home.forms import ProfileForm
from samer.posts.models import post as mongo_post, comment as mongo_comment
from samer.users.context_processors import UserAuth


def home_images(request):
    profile = list(mongo_profile.find(query={}))[0]
    posts = [
        {
            'id': str(post['_id']),
            'name': post['name'],
            'url': post['url'],
            'comments': mongo_comment.count(query={'post': str(post['_id'])}),
            'likes': post['likes'],
            'description': post['description'],
            'type': post['type'],
        }
        for post in mongo_post.find(query={'type': 'image'})
    ]
    return render(request, 'home/home.html', {
        'profile': profile,
        'posts': posts,
    })


def home_videos(request):
    profile = list(mongo_profile.find(query={}))[0]
    posts = [
        {
            'id': str(post['_id']),
            'name': post['name'],
            'thumbnail_url': post['thumbnail_url'],
            'comments': mongo_comment.count(query={'post': str(post['_id'])}),
            'likes': post['likes'],
            'description': post['description'],
            'type': post['type'],
        }
        for post in mongo_post.find(query={'type': 'video'})
    ]
    return render(request, 'home/home.html', {
        'profile': profile,
        'posts': posts,
    })


def home_edit_profile(request):
    user_auth = UserAuth(request)
    profile = list(mongo_profile.find(query={}))[0]
    if not user_auth.is_admin():
        # LANZAR UN ERROR
        return redirect(reverse('users:login'))
    if request.method == 'POST' and 'image_url' in request.FILES:
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            app_name: str = profile_form.cleaned_data['app_name']
            app_real_name: str = profile_form.cleaned_data['app_real_name']
            descriptions: str = profile_form.cleaned_data['descriptions']
            url: str | None = profile_form.cleaned_data['url']
            new_image = profile_form.cleaned_data['image_url']
            new_image_name = str(new_image.name)
            profile_image_name = profile['image_url'].split('/')[-1]
            delete_file(profile_image_name)
            uploaded_file_url = upload_file(
                new_image, object_name=new_image_name
            )
            mongo_profile.delete_one(query={'_id': profile['_id']})
            mongo_profile.create(
                app_name, app_real_name, descriptions=descriptions.splitlines(),
                image_url=uploaded_file_url, url=url
            )
            return redirect(reverse('home:home_images'))
    else:
        profile_form = ProfileForm()
        return render(request, 'home/edit.html', {
            'profile': profile,
            'form': profile_form,
        })
