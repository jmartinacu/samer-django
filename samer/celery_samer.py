import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "samer.samerproject.settings.base",
)

app = Celery("samerproject")


app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "daily-detoxify-comments": {
        "task": "posts.tasks.detoxify_comments",
        "schedule": crontab(hour=0, minute=0),
    },
    "daily-detoxify-questions": {
        "task": "questions.tasks.detoxify_questions",
        "schedule": crontab(hour=0, minute=0),
    },
}
