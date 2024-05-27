import time

from celery import group, shared_task
from django.core.management import call_command

import requests
from celery import shared_task
from sentry_sdk import capture_exception


@shared_task
def check_webpage():
    try:
        response = requests.get("http://127.0.0.1:8001")
        if response.status_code != 200:
            raise Exception(f"Website is down...lets panic!")
    except requests.exceptions.RequestException as e:
        capture_exception(e)


@shared_task
def management_command():
    call_command("test_command")


# @shared_task
# def tp1(queue='celery'):
#     time.sleep(3)
#     return

# @shared_task
# def tp2(queue='celery:1'):
#     time.sleep(3)
#     return

# @shared_task
# def tp3(queue='celery:2'):
#     time.sleep(3)
#     return

# @shared_task
# def tp4(queue='celery:3'):
#     time.sleep(3)
#     return
