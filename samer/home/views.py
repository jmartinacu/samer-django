from bson import ObjectId
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from samer.home.forms import ProfileForm
from samer.home.models import profile as mongo_profile
from samer.posts.models import comment as mongo_comment
from samer.posts.models import post as mongo_post
from samer.posts.models import tag as mongo_tag
from samer.utils import delete_file, upload_file


def home_images(request):
    profile = list(mongo_profile.find(query={}))[0]
    posts = [
        {
            "id": str(post["_id"]),
            "name": post["name"],
            "urls": post["urls"],
            "comments": mongo_comment.count(query={"post": str(post["_id"])}),
            "likes": post["likes"],
            "description": post["description"],
            "type": post["type"],
        }
        for post in mongo_post.find(query={"type": "image"})
    ]
    tags = [
        {
            "id": str(tag["_id"]),
            "url": tag["url"],
            "object_name": tag["object_name"].replace("tags/", ""),
        }
        for tag in mongo_tag.find(query={})
    ]
    return render(
        request,
        "home/home.html",
        {
            "profile": profile,
            "posts": posts,
            "tags": tags,
        },
    )


def home_videos(request):
    profile = list(mongo_profile.find(query={}))[0]
    posts = [
        {
            "id": str(post["_id"]),
            "name": post["name"],
            "thumbnail_url": post["thumbnail_url"],
            "comments": mongo_comment.count(query={"post": str(post["_id"])}),
            "likes": post["likes"],
            "description": post["description"],
            "type": post["type"],
        }
        for post in mongo_post.find(query={"type": "video"})
    ]
    tags = [
        {
            "id": str(tag["_id"]),
            "url": tag["url"],
            "object_name": tag["object_name"].replace("tags/", ""),
        }
        for tag in mongo_tag.find(query={})
    ]
    return render(
        request,
        "home/home.html",
        {
            "profile": profile,
            "posts": posts,
            "tags": tags,
        },
    )


def home_edit_profile(request):
    profile = list(mongo_profile.find(query={}))[0]
    if request.method == "POST" and "image_url" in request.FILES:
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            app_name: str = profile_form.cleaned_data["app_name"]
            app_real_name: str = profile_form.cleaned_data["app_real_name"]
            descriptions: str = profile_form.cleaned_data["descriptions"]
            url: str | None = profile_form.cleaned_data["url"]
            new_image = profile_form.cleaned_data["image_url"]
            new_image_name = str(new_image.name)
            profile_image_name = profile["image_url"].split("/")[-1]
            delete_file(profile_image_name)
            uploaded_file_url = upload_file(
                new_image,
                object_name=new_image_name,
            )
            mongo_profile.delete_one(query={"_id": profile["_id"]})
            mongo_profile.create(
                app_name,
                app_real_name,
                descriptions=descriptions.splitlines(),
                image_url=uploaded_file_url,
                url=url,
            )
            return redirect(reverse("home:home_images"))
    else:
        profile_form = ProfileForm()
        return render(
            request,
            "home/profile.html",
            {
                "profile": profile,
                "form": profile_form,
            },
        )


def home_tag(request, tag_id: str):
    tag = mongo_tag.parse_tag(tag_id)
    if tag is None:
        return redirect(reverse("home:home_images"))
    post_ids = list(map(ObjectId, tag["posts"]))
    posts = [
        {
            "id": str(post["_id"]),
            "name": post["name"],
            "urls": post["urls"],
            "thumbnail_url": post["thumbnail_url"],
            "comments": mongo_comment.count(query={"post": str(post["_id"])}),
            "likes": post["likes"],
            "description": post["description"],
            "type": post["type"],
        }
        for post in mongo_post.find(query={"_id": {"$in": post_ids}})
    ]
    tags = [
        {
            "id": str(tag["_id"]),
            "url": tag["url"],
            "object_name": tag["object_name"].replace("tags/", ""),
        }
        for tag in mongo_tag.find(query={})
    ]
    profile = list(mongo_profile.find(query={}))[0]
    return render(
        request,
        "home/home.html",
        {
            "profile": profile,
            "posts": posts,
            "tags": tags,
        },
    )


def add_message(request):
    level_msg = request.GET.get("level", "info")
    message = request.GET.get("message", "")
    if message == "":
        return JsonResponse(
            {"status": "error", "msg": "Message mandatory"},
            status=400,
        )
    level = messages.INFO
    if level_msg == "success":
        level = messages.SUCCESS
    if level_msg == "warning":
        level = messages.WARNING
    if level_msg == "error":
        level = messages.ERROR
    messages.add_message(request, level, message)
    return JsonResponse({"status": "ok"})
