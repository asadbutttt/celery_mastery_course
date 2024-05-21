# Django Celery Mastery Course

## Docker

Start a new terminal inside a container. Here django is the name of the container:
```
docker exec -it django /bin/sh
```

Create new containers and start in detached mode.
```
docker-compose up -d --build
```

## Celery

Assume there are a few shared tasks of the following format:

```
from celery import shared_task
import time


@shared_task
def tp1():
    time.sleep(3)
    return
```

Task Grouping

```
from celery import group

task_group = group(tp1.s(), tp2.s(), tp3.s(), tp4.s())
task_group.apply_async()
```
Task chaining:
```
from celery import chain

task_chain = chain(tp1.s(), tp2.s(), tp3.s(), tp4.s())
task_chain.apply_async()
```
