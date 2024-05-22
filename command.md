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

Remove all the containers and delete all images:
```
For linux:

docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -aq)

For Windows:

@echo off
echo Stopping all running containers...
for /f "tokens=*" %i in ('docker ps -aq') do docker stop %i

echo Removing all containers...
for /f "tokens=*" %i in ('docker ps -aq') do docker rm %i

echo Removing all images...
for /f "tokens=*" %i in ('docker images -aq') do docker rmi %i

Windows single command:
for /f "tokens=*" %i in ('docker ps -aq') do docker stop %i & for /f "tokens=*" %i in ('docker ps -aq') do docker rm %i & for /f "tokens=*" %i in ('docker images -aq') do docker rmi %i
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
Rabbitmq task testing:
```
from dcelery.celery import t1,t2,t3
t2.apply_async(priority=5)
t1.apply_async(priority=6)
t3.apply_async(priority=9)
t2.apply_async(priority=5)
t1.apply_async(priority=6)
t3.apply_async(priority=9)
```