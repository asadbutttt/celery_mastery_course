import os
import time
from celery import Celery
from kombu import Queue, Exchange
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcelery.settings")
app = Celery("dcelery")
app.config_from_object("django.conf:settings", namespace="CELERY")
sentry_dsn = "https://c79b4ad68d5f9c1a43f2cc59af6d925b@o4507325552132096.ingest.us.sentry.io/4507325554098176"
sentry_sdk.init(dsn=sentry_dsn, integrations=[CeleryIntegration()])

app.conf.task_queues = [
    Queue(
        "tasks",
        Exchange("tasks"),
        routing_key="tasks",
        queue_arguments={"x-max-priority": 10},
    ),
    Queue("dead_letter", routing_key="dead_letter"),
]

app.conf.task_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1

base_dir = os.getcwd()
task_folder = os.path.join(base_dir, "dcelery", "celery_tasks")

if os.path.exists(task_folder) and os.path.isdir(task_folder):
    task_modules = []
    for filename in os.listdir(task_folder):
        if filename.startswith("ex") and filename.endswith(".py"):
            module_name = f"dcelery.celery_tasks.{filename[:-3]}"

            module = __import__(module_name, fromlist=["*"])

            for name in dir(module):
                obj = getattr(module, name)
                if callable(obj) and name.startswith("my_tasks"):
                    task_modules.append(f"{module_name}.{name}")

    app.autodiscover_tasks(task_modules)
