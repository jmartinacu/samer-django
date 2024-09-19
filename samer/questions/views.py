import json

from bson import ObjectId
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from samer.questions.forms import CreateQuestionAnswerForm, CreateQuestionForm
from samer.questions.models import question as mongo_question
from samer.users.context_processors import UserAuth


def questions(request):
    option = request.GET.get("option", "")
    search = request.GET.get("search", "")
    if option == "author":
        query = {"author": {"$regex": f"^{search}", "$options": "i"}}
    elif option == "content":
        query = {"content": {"$regex": f"{search}", "$options": "i"}}
    elif option == "title":
        query = {"title": {"$regex": f"{search}", "$options": "i"}}
    elif option == "tag":
        query = {"tags": {"$in": [f"{search}"]}}
    elif option == "resolved":
        query = {"resolve": True}
    else:
        query = {}
    query["toxic"] = False
    questions_db = mongo_question.get_questions_sorted_by_likes(
        query=query,
    )
    questions = [
        {
            "id": str(q["_id"]),
            "title": q["title"],
            "content": q["content"],
            "author": q["author"],
            "resolve": q["resolve"],
            "answer": q["answer"]["text"] if q["answer"] else None,
            "likes": q["likes"],
            "tags": q["tags"],
            "views": q["views"],
        }
        for q in list(questions_db)
    ]
    return render(
        request,
        "questions/questions_content.html",
        {"questions": questions},
    )


def question(request, question_id):
    user_auth = UserAuth(request)
    question = mongo_question.parse_question(question_id)
    if question is None:
        messages.error(
            request,
            "Pregunta no encontrada",
        )
        return redirect(reverse("questions:questions"))
    if user_auth.is_login():
        if user_auth.user_auth["id"] not in question["views"]:
            views = mongo_question.add_view(
                question,
                user_auth.user_auth["id"],
            )
            question["views"] = views
    return render(request, "questions/question.html", {"question": question})


def create(request):
    user_auth = UserAuth(request)
    if not user_auth.is_login():
        messages.warning(
            request,
            "Tienes tener una cuenta para crear una pregunta",
        )
        return redirect(reverse("users:login"))
    if request.method == "POST":
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            tags: str = form.cleaned_data["tags"]
            author = form.cleaned_data["author"]
            tags = tags.split(",")
            unresolved_questions = mongo_question.get_unresolved(
                username=author,
            )
            if len(unresolved_questions) > 0:
                messages.warning(
                    request,
                    "No se puede crear una nueva pregunta, ya hay una en curso",  # noqa
                )
                return redirect(reverse("questions:questions"))
            mongo_question.create(
                title=title, content=content, author=author, tags=tags
            )
            return redirect(reverse("questions:questions"))
        else:
            return render(request, "questions/create.html", {"form": form})
    else:
        title = request.GET.get("title", None)
        content = request.GET.get("content", None)
        form = CreateQuestionForm(
            title=title,
            content=content,
            username=user_auth.user_auth["username"],
        )
        return render(request, "questions/create.html", {"form": form})


def delete(request, question_id):
    user_auth = UserAuth(request)
    if not user_auth.is_login():
        messages.warning(request, "Necesitas tener una sesión")
        return redirect(reverse("users:login"))
    question = mongo_question.find_one(
        {
            "_id": ObjectId(question_id),
        }
    )
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("questions:questions"))
    if question["author"] != user_auth.user_auth["username"]:
        messages.warning(request, "No tienes permisos para esta acción")
        return redirect(reverse("questions:questions"))
    mongo_question.delete_questions([question])
    return redirect(reverse("questions:questions"))


def add_remove_like(request, question_id):
    user_auth = UserAuth(request)
    if not user_auth.is_login():
        messages.warning(request, "Necesitas tener una sesión")
        return redirect(reverse("users:login"))
    question = mongo_question.find_one(
        {
            "_id": ObjectId(question_id),
        },
    )
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("questions:questions"))
    mongo_question.add_or_remove_likes(
        question,
        [user_auth.user_auth["id"]],
    )
    return redirect(reverse("questions:question", args=[question_id]))


def create_answer(request, question_id, edit):
    user_auth = UserAuth(request)
    question = mongo_question.parse_question(question_id)
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    if question["resolve"] and not bool(edit):
        messages.info(request, "Pregunta ya resuelta")
        return redirect(reverse("root:questions"))
    if request.method == "POST":
        form = CreateQuestionAnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data["answer"]
            admin = form.cleaned_data["admin"]
            mongo_question.add_answer(
                question_id,
                answer={
                    "admin": admin,
                    "text": answer,
                },
            )
            question = mongo_question.parse_question(question_id)
            return redirect(
                reverse("root:question_details", args=[question["id"]]),
            )
        else:
            return render(
                request,
                "root/questions/create_answer.html",
                {"form": form, "edit": edit, "question": question},
            )
    else:
        form = CreateQuestionAnswerForm(
            admin=user_auth.user_auth["username"],
            question=question["content"],
        )
        return render(
            request,
            "root/questions/create_answer.html",
            {"form": form, "edit": edit, "question": question},
        )


def delete_root(request, question_id):
    question = mongo_question.find_one(
        {
            "_id": ObjectId(question_id),
        }
    )
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    mongo_question.delete_questions([question])
    return redirect(reverse("root:questions"))


def archive(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question_ids = data.get("question_ids", [])
        mongo_question.archive_unarchive_questions(question_ids)
        return redirect(reverse("root:questions"))


def add_remove_toxic(request, question_id: str):
    question = mongo_question.parse_question(question_id)
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    mongo_question.add_remove_toxic([question])
    return redirect(reverse("root:question_details", args=[question_id]))
