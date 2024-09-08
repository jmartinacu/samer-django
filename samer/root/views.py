import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from bson import ObjectId

from samer.utils import upload_file
from samer.posts.models import (
    post as mongo_post,
    comment as mongo_comment,
    tag as mongo_tag,
    ParsedComment,
)
from samer.posts.utils import get_mime_type_from_urls
from samer.users.context_processors import UserAuth
from samer.users.models import (
    user as mongo_user,
    ParsedUser,
)
from samer.users import hashing
from samer.questions.models import question as mongo_question
from samer.root.forms import (
    UploadPost,
    EditPost,
    AdminForm,
    CreateTag,
)
from samer.root.utils import create_post, edit_post as edit_post_utility


def root(request):
    posts_db = mongo_post.find(query={})
    posts = [
        {
            "id": str(post["_id"]),
            "name": post["name"],
            "comments": mongo_comment.count(query={"post": str(post["_id"])}),
            "likes": post["likes"],
            "type": "imagen" if post["type"] == "image" else "video",
            "tags": ", ".join(
                [
                    tag["name"]
                    for tag in mongo_tag.find(
                        query={"posts": str(post["_id"])},
                    )
                ]
            ),
        }
        for post in posts_db
    ]
    return render(
        request,
        "root/posts/posts.html",
        {
            "posts": posts,
        },
    )


def users(request):
    users = [
        {
            "id": str(user["_id"]),
            "admin": user["admin"],
            "name": user["name"],
            "surname": user["surname"],
            "email": user["email"],
            "username": user["username"],
        }
        for user in mongo_user.find(query={})
    ]
    return render(
        request,
        "root/users/users.html",
        {"users": users},
    )


def tags(request):
    tags = [
        {
            "id": str(tag["_id"]),
            "name": tag["name"],
            "posts": tag["posts"],
        }
        for tag in mongo_tag.find(query={})
    ]
    return render(
        request,
        "root/tags/tags.html",
        {
            "tags": tags,
        },
    )


def questions(request):
    questions = [
        {
            "id": str(question["_id"]),
            "title": question["title"],
            "author": question["author"],
            "resolve": question["resolve"],
            "archive": question["archive"],
            "likes": question["likes"],
        }
        for question in mongo_question.find(query={})
    ]
    return render(
        request,
        "root/questions/questions.html",
        {
            "questions": questions,
        },
    )


def tag_details(request, tag_id):
    tag = mongo_tag.parse_tag(tag_id)
    if tag is None:
        return redirect(reverse("root:tags"))
    tag["posts"] = [
        {
            "id": str(post["_id"]),
            "name": post["name"],
            "type": "imagen" if post["type"] == "image" else "video",
        }
        for post in mongo_post.find(
            query={"_id": {"$in": list(map(ObjectId, tag["posts"]))}}
        )
    ]
    return render(
        request,
        "root/tags/tag.html",
        {"tag": tag, "posts_json": json.dumps(tag["posts"])},
    )


def question_details(request, question_id):
    question = mongo_question.parse_question(question_id)
    if question is None:
        messages.ero
        return redirect(reverse("root:questions"))
    return render(
        request,
        "root/questions/question.html",
        {"question": question},
    )


def create_admin(request):
    if request.method == "POST":
        form = AdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["user"]
            email = form.cleaned_data["email"]
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            password = form.cleaned_data["pwd"]
            hashed_pwd = hashing.hash_password(password)
            try:
                users = mongo_user.find(query={"username": username})
                if len(list(users)) > 0:
                    messages.warning(request, "El nombre de usuario ya existe")
                    return render(
                        request,
                        "root/users/create.html",
                        {
                            "admin_form": form,
                        },
                    )
                mongo_user.create(
                    username=username,
                    password=hashed_pwd,
                    email=email,
                    name=name,
                    surname=surname,
                    admin=True,
                )
                return redirect(reverse("root:users"))
            except Exception as e:
                messages.error(request, f"Algo ha fallado: {e}")
                return render(
                    request,
                    "root/users/create.html",
                    {
                        "admin_form": form,
                    },
                )
    else:
        form = AdminForm()
    return render(
        request,
        "root/users/create.html",
        {
            "admin_form": form,
        },
    )


def user_details(request, user_id):
    user: ParsedUser | None = mongo_user.parsed_user(user_id)
    if user is None:
        messages.error(request, "Usuario no encontrado")
        return redirect(reverse("root:users"))
    comments: list[ParsedComment] = mongo_comment.find(
        {
            "author": user_id,
        }
    )
    return render(
        request,
        "root/users/user.html",
        {
            "user": user,
            "comments": comments,
        },
    )


def post_details(request, post_id):
    post_db = mongo_post.parse_post(post_id)
    if post_db is None:
        messages.error(request, "Publicación no encontrada")
        return redirect(reverse("root:root"))
    comments = list(
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
    )
    post_db["mime_type"] = get_mime_type_from_urls(post_db["urls"])
    return render(
        request,
        "root/posts/post.html",
        {
            "post": post_db,
            "comments": comments,
        },
    )


def upload_post(request):
    if request.method == "POST":
        form = UploadPost(request.POST, request.FILES)
        if form.is_valid():
            result = create_post(
                files=form.cleaned_data["file"],
                name=form.cleaned_data["name"],
                des=form.cleaned_data["des"],
            )
            if "error" in result:
                upload_post = render(
                    request,
                    "root/posts/create.html",
                    {"image_post_form": form},
                )
                if result["status"] == "DuplicateName":
                    messages.warning(
                        request,
                        "Ya hay una publicación con ese nombre",
                    )
                    return upload_post
                elif result["status"] == "NotImageOrVideo":
                    messages.warning(
                        request,
                        "El archivo tiene que ser una imagen o video",
                    )
                    return upload_post
                elif result["status"] == "MoreThanOneVideo":
                    messages.warning(
                        request,
                        "Solamente se puede subir un video por publicación",
                    )
                    return upload_post
                elif result["status"] == "MixedVideoAndImage":
                    messages.warning(
                        request,
                        "No se pueden subir videos e imágenes a la vez",
                    )
                    return upload_post
                else:
                    return render("root:root")
            return redirect(
                reverse("root:post_details", kwargs={"post_id": result["id"]})
            )
        else:
            return render(
                request,
                "root/posts/create.html",
                {"image_post_form": form},
            )
    else:
        form = UploadPost()
        return render(
            request,
            "root/posts/create.html",
            {"image_post_form": form},
        )


def delete_post(request, post_id):
    post_db = mongo_post.find_one(query={"_id": ObjectId(post_id)})
    if post_db is None:
        messages.error(request, "Publicación no encontrada")
        return redirect(reverse("root:root"))
    mongo_post.delete_posts([post_db])
    return redirect(reverse("root:root"))


def edit_post(request, post_id):
    post_db = mongo_post.parse_post(post_id)
    if post_db is None:
        messages.error(request, "Publicación no encontrada")
        return redirect(reverse("root:root"))
    if request.method == "POST":
        form = EditPost(request.POST, request.FILES)
        if form.is_valid():
            fls = form.cleaned_data["file"] if "file" in request.FILES else []
            result = edit_post_utility(
                files=fls,
                des=form.cleaned_data["des"],
                name=form.cleaned_data["name"],
                post=post_db,
            )
            if "error" in result:
                form = EditPost(post=post_db)
                render_edit = render(
                    request,
                    "root/posts/edit.html",
                    {
                        "edit_post_form": form,
                        "post": post_db,
                    },
                )
                if result["status"] == "NotImageOrVideo":
                    messages.warning(
                        request,
                        "El archivo tiene que ser una imagen o video",
                    )
                    return render_edit
                elif result["status"] == "MoreThanOneVideo":
                    messages.warning(
                        request,
                        "Solamente se puede subir un video por publicación",
                    )
                    return render_edit
                elif result["status"] == "MixedVideoAndImage":
                    messages.warning(
                        request,
                        "No se pueden subir videos e imágenes a la vez",
                    )
                    return render_edit
                else:
                    return render("root:root")
            return redirect(
                reverse(
                    "root:post_details",
                    kwargs={"post_id": post_id},
                )
            )
        else:
            form = EditPost(post=post_db)
            return render(
                request,
                "root/posts/edit.html",
                {
                    "edit_post_form": form,
                    "post": post_db,
                },
            )
    else:
        form = EditPost(post=post_db)
        return render(
            request,
            "root/posts/edit.html",
            {
                "edit_post_form": form,
                "post": post_db,
            },
        )


def delete_comment(request, post_id, comment_id):
    mongo_comment.delete_one({"_id": ObjectId(comment_id)})
    return redirect(reverse("root:post_details", args=[post_id]))


def delete_tag(request, tag_id):
    mongo_tag.delete_tags(
        list(mongo_tag.find(query={"_id": ObjectId(tag_id)})),
    )
    return redirect(reverse("root:tags"))


def delete_action(request, model):
    user_auth = UserAuth(request)
    if request.method == "POST":
        referrer_url = request.META.get("HTTP_REFERER", "/")
        if model not in settings.AUTH_ACTION_MODELS:
            messages.error(request, "Acción no permitida")
            return redirect(referrer_url)
        data = json.loads(request.body)
        selected_ids = data.get("delete_ids", [])
        ids = list(map(ObjectId, selected_ids))
        if user_auth.user_auth["id"] in selected_ids:
            messages.warning(
                request,
                "No puedes borrar al usuario que realiza la acción",
            )
            return redirect(referrer_url)
        if model == "User":
            mongo_user.delete_users(
                list(mongo_user.find(query={"_id": {"$in": ids}})),
            )
        elif model == "Post":
            mongo_post.delete_posts(
                list(mongo_post.find(query={"_id": {"$in": ids}})),
            )
        elif model == "Tag":
            mongo_tag.delete_tags(
                list(mongo_tag.find(query={"_id": {"$in": ids}})),
            )
        elif model == "Question":
            mongo_question.delete_questions(
                list(mongo_question.find(query={"_id": {"$in": ids}})),
            )
        messages.success(request, "Acción completada")
        return redirect(referrer_url)
    else:
        messages.warning(request, "Acción incorrecta")
        return redirect(reverse("root:root"))


def tag_action(request):
    if request.method == "POST" and "file" in request.FILES:
        form = CreateTag(request.POST, request.FILES)
        if form.is_valid():
            name: str = form.cleaned_data["name"]
            ids: str = form.cleaned_data["ids"]
            post_ids = ids.split(",")
            file = form.cleaned_data["file"]
            file_name = str(file.name)
            object_name = f"tags/{file_name}"
            uploaded_file_url = upload_file(
                file,
                object_name=object_name,
            )
            mongo_tag.create(
                name=name,
                url=uploaded_file_url,
                object_name=object_name,
                posts=post_ids,
            )
            return redirect(reverse("root:root"))
        return redirect("root:root")
    elif request.method == "GET":
        post_ids = request.GET.get("post_ids", [])
        post_ids = post_ids.split(",")
        posts_db = mongo_post.find(
            query={"_id": {"$in": list(map(ObjectId, post_ids))}}
        )
        posts = [
            {
                "id": str(post["_id"]),
                "name": post["name"],
                "type": "imagen" if post["type"] == "image" else "video",
            }
            for post in posts_db
        ]
        form = CreateTag(
            ids=",".join(list(map(lambda p: p["id"], posts))),
            init=True,
        )
        return render(
            request,
            "root/tags/create.html",
            {
                "form": form,
                "posts": posts,
            },
        )
    else:
        return redirect(reverse("root:root"))
