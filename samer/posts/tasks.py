from celery import shared_task

from samer.detoxify_samer import predict_detoxify
from samer.posts.models import comment as mongo_comment


@shared_task
def detoxify_comments():
    comments = mongo_comment.parse_comments(
        list(mongo_comment.find({"moderate": False})),
    )
    if len(comments) == 0:
        return
    data = [comment["text"] for comment in comments]
    detoxify_res = predict_detoxify(data)
    toxic = set(
        [t[0] for key in detoxify_res for t in detoxify_res[key]["info"]],
    )
    toxic_comments = list(
        filter(
            lambda c: c["text"] in toxic,
            comments,
        ),
    )
    toxic_ids = [q["id"] for q in toxic_comments]
    non_toxic_comments = [q for q in comments if q["id"] not in toxic_ids]
    mongo_comment.apply_detoxify(
        toxic_comments,
        non_toxic_comments,
    )
