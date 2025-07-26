import os
import sys
from pathlib import Path

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))


# init celery
app = Celery(
    "followers",
    broker=os.getenv("CELERY_BROKER"),
    backend=os.getenv("CELERY_BACKEND"),
    include=["celery_app.tasks"]
)


# setting schedule
app.conf.beat_schedule = {
    "request_followers_youtube": {
        "task": "celery_app.tasks.youtube_api",
        "schedule": crontab(hour=13, minute=54)
    },
    "request_followers_vk": {
        "task": "celery_app.tasks.vk_api",
        "schedule": crontab(minute="*/5")
    }
}
