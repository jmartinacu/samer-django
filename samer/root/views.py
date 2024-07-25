from os import path

from django.shortcuts import render, redirect
from django.urls import reverse

from samer.utils import upload_file
from samer.posts.models import (
    post as mongo_post,
    comment as mongo_comment,
    PostTypes,
)
from samer.posts.utils import is_image, is_video, upload_thumbnail
from samer.root.forms import UploadImagePost


def root(request):
    posts_db = mongo_post.find(query={})
    posts = [
        {
            "id": str(post["_id"]),
            "name": post["name"],
            "comments": mongo_comment.count(query={"post": str(post["_id"])}),
            "likes": post["likes"],
            "type": "imagen" if post["type"] == "image" else "video",
        }
        for post in posts_db
    ]
    return render(
        request,
        "root/post.html",
        {
            "posts": posts,
        },
    )


def upload_image_post(request):
    if request.method == "POST":
        form = UploadImagePost(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.cleaned_data["file"]
            post_bytes = new_post.read()
            new_post.seek(0)
            post_des = form.cleaned_data["des"]
            post_name = str(new_post.name)
            name, _ext = path.splitext(post_name)
            if is_image(post_bytes):
                object_name = f"imagenes/{post_name}"
                uploaded_file_url = upload_file(
                    new_post,
                    object_name=object_name,
                )
                mongo_post.create(
                    name=name,
                    object_name=object_name,
                    url=uploaded_file_url,
                    description=post_des,
                    type=PostTypes.IMAGE,
                )
                return redirect(reverse("root:root"))
            elif is_video(post_bytes):
                object_name = f"videos/{post_name}"
                uploaded_file_url = upload_file(
                    new_post,
                    object_name=object_name,
                )
                thumbnail = upload_thumbnail(0, uploaded_file_url)
                mongo_post.create(
                    name=name,
                    object_name=object_name,
                    url=uploaded_file_url,
                    description=post_des,
                    type=PostTypes.VIDEO,
                    thumbnail_url=thumbnail,
                )
                return redirect(reverse("root:root"))
            else:
                print("no es imagen ni video")
                print(post_name)
                return redirect(reverse("root:root"))
        else:
            return render(
                request,
                "root/upload_post.html",
                {"image_post_form": form},
            )
    else:
        form = UploadImagePost()
        return render(
            request,
            "root/upload_post.html",
            {"image_post_form": form},
        )
