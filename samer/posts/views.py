import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from bson import ObjectId

from samer.posts.forms import CreateCommentForm
from samer.posts.models import (
    Post,
    post as mongo_post,
    comment as mongo_comment,
    tag as mongo_tag,
)
from samer.posts.utils import get_mime_type_from_urls
from samer.users.context_processors import UserAuth
from samer.users.models import user as mongo_user


def add_remove_like(request, post_id):
    user_auth = UserAuth(request)
    if not user_auth.is_login():
        # LANZAR ERROR NO AUTORIZADO
        return redirect(reverse("home:home_images"))
    post: Post | None = mongo_post.find_one(query={"_id": ObjectId(post_id)})
    if post is None:
        # EN VEZ DE UN ERROR PODRIA SOLTAR UN WARNING EN LA PANTALLA
        return render(request, "home/home.html", {"error": "Post not found"})
    if user_auth.user_auth["id"] in post["likes"]:
        mongo_post.update_one(
            filter={"_id": ObjectId(post_id)},
            update={
                "$set": {
                    "likes": [
                        like
                        for like in post["likes"]
                        if like != user_auth.user_auth["id"]
                    ]
                }
            },
        )
    else:
        mongo_post.update_one(
            filter={"_id": ObjectId(post_id)},
            update={
                "$set": {"likes": post["likes"] + [user_auth.user_auth["id"]]},
            },
        )
    if post["type"] == "image":
        return redirect(reverse("home:home_images"))
    else:
        return redirect(reverse("home:home_videos"))


def comments(request, post_id: str, post_type: str):
    user_auth = UserAuth(request)
    if request.method == "POST":
        if not user_auth.is_login():
            # LANZAR ERROR QUE NO ESTA AUTORIZADO
            return redirect(reverse("home:home_images"))
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data["comment"]
            author = user_auth.user_auth["id"]
            mongo_comment.create(post_id, author, comment)
            post_db = mongo_post.find_one(query={"_id": ObjectId(post_id)})
            if post_db is None:
                # DEBERIA DE LANZAR UN ERROR AL USUARIO
                return redirect(reverse("home:home_images"))
            post = {
                "id": str(post_db["_id"]),
                "name": post_db["name"],
                "urls": post_db["urls"],
                "likes": post_db["likes"],
                "description": post_db["description"],
                "type": post_db["type"],
                "mime_type": get_mime_type_from_urls(post_db["urls"]),
            }
            comments = [
                {
                    "id": str(comment["_id"]),
                    "post": comment["post"],
                    "author": mongo_user.parsed_user(
                        comment["author"],
                    ),
                    "created_at": comment["created_at"],
                    "text": comment["text"],
                }
                for comment in mongo_comment.find(query={"post": post_id})
            ]
            comment_form = CreateCommentForm()
            template = ""
            if post_type == "image":
                template = "posts/image.html"
            elif post_type == "video":
                template = "posts/video.html"
            else:
                # LANZAR ERROR TYPE INCORRECTO
                return redirect(reverse("home:home_images"))
            return render(
                request,
                template,
                {
                    "post": post,
                    "comments": comments,
                    "form": comment_form,
                },
            )
    else:
        post_db = mongo_post.find_one(query={"_id": ObjectId(post_id)})
        if post_db is None:
            # DEBERIA DE LANZAR UN ERROR AL USUARIO
            return redirect(reverse("home:home_images"))
        post = {
            "id": str(post_db["_id"]),
            "name": post_db["name"],
            "urls": post_db["urls"],
            "comments": mongo_comment.count(
                query={"post": str(post_db["_id"])},
            ),
            "likes": post_db["likes"],
            "description": post_db["description"],
            "type": post_db["type"],
            "mime_type": get_mime_type_from_urls(post_db["urls"]),
        }
        comment_form = CreateCommentForm()
        comments = [
            {
                "id": str(comment["_id"]),
                "post": comment["post"],
                "author": mongo_user.parsed_user(
                    comment["author"],
                ),
                "created_at": comment["created_at"],
                "text": comment["text"],
            }
            for comment in mongo_comment.find(query={"post": post_id})
        ]
        template = ""
        if post_type == "image":
            template = "posts/image.html"
        elif post_type == "video":
            template = "posts/video.html"
        else:
            # LANZAR ERROR TYPE INCORRECTO
            return redirect(reverse("home:home_images"))
        return render(
            request,
            template,
            {
                "post": post,
                "comments": comments,
                "form": comment_form,
            },
        )


def remove_comment(request, post_id: str, comment_id: str):
    user_auth = UserAuth(request)
    comment_db = mongo_comment.find_one({"_id": ObjectId(comment_id)})
    post_db = mongo_post.find_one(query={"_id": ObjectId(post_id)})
    if post_db is None:
        # DEBERIA DE LANZAR UN ERROR AL USUARIO
        return redirect(reverse("home:home_images"))
    if comment_db is None:
        # LANZAR ERROR NO ENCONTRADO
        return redirect(
            reverse("posts:comment", args=[post_id, post_db["type"]]),
        )
    if not comment_db["author"] == user_auth.user_auth["id"]:
        # LANZAR ERROR NO AUTORIZADO
        return redirect(reverse("home:home_images"))
    mongo_comment.delete_one({"_id": ObjectId(comment_id)})
    post = {
        "id": str(post_db["_id"]),
        "name": post_db["name"],
        "urls": post_db["urls"],
        "comments": mongo_comment.count(query={"post": str(post_db["_id"])}),
        "likes": post_db["likes"],
        "description": post_db["description"],
        "type": post_db["type"],
        "mime_type": get_mime_type_from_urls(post_db["urls"]),
    }
    comment_form = CreateCommentForm()
    comments = mongo_comment.find(query={"post": post_id})
    template = ""
    if post["type"] == "image":
        template = "posts/image.html"
    elif post["type"] == "video":
        template = "posts/video.html"
    else:
        # LANZAR ERROR TYPE INCORRECTO
        return redirect(reverse("home:home_images"))
    return render(
        request,
        template,
        {
            "post": post,
            "comments": [
                {
                    "id": str(comment["_id"]),
                    "post": comment["post"],
                    "author": comment["author"],
                    "created_at": comment["created_at"],
                    "text": comment["text"],
                }
                for comment in comments
            ],
            "form": comment_form,
        },
    )


def search_posts(request):
    post_name = request.GET.get("post_name", "")
    if post_name == "":
        return JsonResponse([], safe=False)
    posts_db = mongo_post.find(
        query={"name": {"$regex": f"^{post_name}", "$options": "i"}},
    )
    posts = [
        {
            "id": str(post["_id"]),
            "name": post["name"],
            "urls": post["urls"],
            "likes": post["likes"],
            "description": post["description"],
            "type": post["type"],
        }
        for post in posts_db
    ]
    return JsonResponse(posts, safe=False)


def add_post_to_tag(request, tag_id: str):
    user_auth = UserAuth(request)
    if not user_auth.is_admin():
        # LANZAR UN ERROR
        return redirect(reverse("users:login"))
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post_ids = data.get("post_ids", [])
            tag = mongo_tag.find_one({"_id": ObjectId(tag_id)})
            if tag is None:
                # LANZAR ERROR
                return redirect(reverse("root:tags"))
            mongo_tag.add_posts(tag, post_ids)
            return redirect(reverse("root:tag_details", args=[tag_id]))
        except ValueError as e:
            # LANZAR ERROR INFORME AL USUARIO
            e = e
            return redirect(reverse("root:tags"))
