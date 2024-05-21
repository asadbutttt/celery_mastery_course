from celery import Celery
from newapp.tasks import task2

app = Celery("task")
app.config_from_object("celeryconfig")
app.conf.imports = "newapp.tasks"
app.autodiscover_tasks()
