import json

from bson import ObjectId
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from samer.posts.forms import CreateCommentForm
from samer.posts.models import Post
from samer.posts.models import comment as mongo_comment
from samer.posts.models import post as mongo_post
from samer.posts.models import tag as mongo_tag
from samer.posts.tasks import detoxify_comments
from samer.posts.utils import get_mime_type_from_urls
from samer.users.context_processors import UserAuth


def add_remove_like(request, post_id):
    allows_redirects = [
        "home:home_images",
        "home:home_videos",
        "posts:comment",
    ]
    user_auth = UserAuth(request)
    redirect_view = request.GET.get("redirect", "home:home_images")
    post_type = None
    if redirect_view not in allows_redirects:
        messages.error(request, f"Redirección {redirect_view} no permitida")
    if redirect_view == "posts:comment":
        post_type: str = request.GET.get("type", "")
        if post_type == "" or post_type not in ["image", "video"]:
            messages.error(request, "Tipo de publicación incorrecto")
            return redirect(reverse("home:home_images"))
    post: Post | None = mongo_post.find_one(query={"_id": ObjectId(post_id)})
    if post is None:
        messages.error(request, "Publicación no encontrada")
        if post_type:
            return redirect(reverse(redirect_view, args=[post_id, post_type]))
        return redirect(reverse(redirect_view))
    if not user_auth.is_login():
        messages.warning(
            request,
            "Tienes tener una cuenta para dar un me gusta",
        )
        if post_type:
            return redirect(reverse(redirect_view, args=[post_id, post_type]))
        return redirect(reverse(redirect_view))
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
    if post_type:
        return redirect(reverse(redirect_view, args=[post_id, post_type]))
    return redirect(reverse(redirect_view))


# CREAR UN VALIDADOR CUSTOM DEL POST_ID QUE SEA UN OBJECTID VALIDO
def comments(request, post_id: str, post_type: str):
    user_auth = UserAuth(request)
    template = ""
    if post_type == "image":
        template = "posts/image.html"
    elif post_type == "video":
        template = "posts/video.html"
    else:
        messages.error(request, "Tipo de publicación incorrecto")
        return redirect(reverse("home:home_images"))
    post_db = mongo_post.find_one(query={"_id": ObjectId(post_id)})
    if post_db is None:
        messages.error(request, "Publicación no encontrada")
        if post_type == "video":
            return redirect(reverse("home:home_videos"))
        else:
            return redirect(reverse("home:home_images"))
    if request.method == "POST":
        if not user_auth.is_login():
            messages.error(
                request,
                "Hay que tener una sesión creada e iniciada",
            )
            return redirect(
                reverse(
                    "posts:comment",
                    args=[post_id, post_type],
                )
            )
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data["comment"]
            author = user_auth.user_auth["id"]
            mongo_comment.create(post_id, author, comment)
    post = {
        "id": str(post_db["_id"]),
        "name": post_db["name"],
        "urls": post_db["urls"],
        "likes": post_db["likes"],
        "description": post_db["description"],
        "type": post_db["type"],
        "mime_type": get_mime_type_from_urls(post_db["urls"]),
    }
    comment_form = CreateCommentForm()
    comments = mongo_comment.parse_comments(
        list(mongo_comment.find(query={"post": post_id, "toxic": False})),
    )
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
    post_db = mongo_post.find_one(query={"_id": ObjectId(post_id)})
    if post_db is None:
        messages.error(request, "Publicación no encontrada")
        return redirect(reverse("home:home_videos"))
    comment_db = mongo_comment.find_one({"_id": ObjectId(comment_id)})
    if comment_db is None:
        messages.error(request, "Comentario no encontrado")
        return redirect(
            reverse("posts:comment", args=[post_id, post_db["type"]]),
        )
    if not comment_db["author"] == user_auth.user_auth.get("id", ""):
        messages.error(request, "El comentario no puede ser eliminado")
        return redirect(
            reverse("posts:comment", args=[post_id, post_db["type"]]),
        )
    mongo_comment.delete_comments([comment_db])
    post = {
        "id": str(post_db["_id"]),
        "name": post_db["name"],
        "urls": post_db["urls"],
        "likes": post_db["likes"],
        "description": post_db["description"],
        "type": post_db["type"],
        "mime_type": get_mime_type_from_urls(post_db["urls"]),
    }
    comment_form = CreateCommentForm()
    comments = mongo_comment.parse_comments(
        list(mongo_comment.find(query={"post": post_id, "toxic": False})),
    )
    template = "posts/image.html"
    if post_db["type"] == "video":
        template = "posts/video.html"
    return render(
        request,
        template,
        {
            "post": post,
            "comments": comments,
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
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post_ids = data.get("post_ids", [])
            tag = mongo_tag.find_one({"_id": ObjectId(tag_id)})
            if tag is None:
                messages.error(request, "Etiqueta no encontrada")
                return redirect(reverse("root:tags"))
            mongo_tag.add_posts(tag, post_ids)
            return redirect(reverse("root:tag_details", args=[tag_id]))
        except ValueError as e:
            messages.warning(request, str(e))
            return redirect(reverse("root:tags"))


def test_detoxify_comments(request):
    comments = mongo_comment.parse_comments(
        list(mongo_comment.find(query={}, limit=10))
    )
    print(comments)
    detoxify_comments.delay(comments)
    return redirect(reverse("home:home_images"))
