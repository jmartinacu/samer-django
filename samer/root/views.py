from django.shortcuts import render, redirect
from django.urls import reverse

from samer.utils import upload_file
from samer.posts.models import post as mongo_post
from samer.root.forms import UploadImagePost


def root(request):
    return render(request, 'root/post.html')


def upload_image_post(request):
    if request.method == 'POST':
        form = UploadImagePost(request.POST, request.FILES)
        if form.is_valid():
            print('formulario valido')
            new_post = form.cleaned_data['image_post']
            name = form.cleaned_data['name']
            object_name = f'imagenes/{name}'
            uploaded_file_url = upload_file(new_post, object_name=object_name)
            mongo_post.create(
                name=name, object_name=object_name, url=uploaded_file_url
            )
            return redirect(reverse('root:root'))
        else:
            return render(request, 'root/upload_post.html', {
                'image_post_form': form
            })
    else:
        form = UploadImagePost()
        return render(request, 'root/upload_post.html', {
            'image_post_form': form
        })
