from celery import shared_task

from samer.detoxify_samer import predict_detoxify
from samer.questions.models import question as mongo_question


@shared_task
def detoxify_questions():
    questions = mongo_question.parse_questions(
        list(mongo_question.find({"moderate": False}))
    )
    if len(questions) == 0:
        return
    data = []
    for question in questions:
        data.append(question["title"])
        data.append(question["content"])
    detoxify_res = predict_detoxify(data)
    toxic = set(
        [t[0] for key in detoxify_res for t in detoxify_res[key]["info"]],
    )
    toxic_questions = list(
        filter(
            lambda q: q["title"] in toxic or q["content"] in toxic,
            questions,
        ),
    )
    toxic_ids = [q["id"] for q in toxic_questions]
    non_toxic_questions = [q for q in questions if q["id"] not in toxic_ids]
    mongo_question.apply_detoxify(
        toxic_questions,
        non_toxic_questions,
    )
