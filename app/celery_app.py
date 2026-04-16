# app/celery_app.py
from celery import Celery
from app.core.config import settings
from app.core.vector_provider import init_vector_db
from app.core.llm_provider import init_llm
from asgiref.sync import async_to_sync
from celery.signals import worker_process_init


@worker_process_init.connect
def setup_vector_db(*args, **kwargs):
    # Bridge the async init to the sync worker process startup
    async_to_sync(init_llm)()
    async_to_sync(init_vector_db)()


app = Celery(
    "apexstore_ai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# This tells Celery to look for 'tasks' folders or modules
# inside the specified packages automatically.
app.autodiscover_tasks(["app.tasks"])
