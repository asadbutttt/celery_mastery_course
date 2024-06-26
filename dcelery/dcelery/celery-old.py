@app.task(queue="tasks")
def t1(a, b, message=None):
    result = a + b
    if message:
        result = f"{message}: {result}"
    return


@app.task(queue="tasks")
def t2():
    time.sleep(5)
    return


@app.task(queue="tasks")
def t3():
    time.sleep(5)
    return


# app.conf.task_routes = {
#     "newapp.tasks.task1": {"queue": "queue1"},
#     "newapp.tasks.task2": {"queue": "queue2"},
# }

# app.cnof.task_default_rate_limit = "1/m"

# app.conf.broker_transport_options = {
#     "priority_steps": list(range(10)),
#     "sep": ":",
#     "queue_order_strategy": "priority",
# }

app.autodiscover_tasks()


def test():
    # Call the task asynchronously
    result = t1.apply_async(args=[5, 10], kwargs={"message": "The sum is"})

    # Check if the task has completed
    if result.ready():
        print("Task has completed")
    else:
        print("Task is still running")

    # Check if the task completed successfully
    if result.successful():
        print("Task completed successfully")
    else:
        print("Task encountered an error")

    # Get the result of the task
    try:
        task_result = result.get()
        print("Task result:", task_result)
    except Exception as e:
        print("An exception occurred:", str(e))

    # Get the exception (if any) that occurred during task execution
    exception = result.get(propagate=False)
    if exception:
        print("An exception occurred during task execution:", str(exception))


# Synchronous task execution
def execute_sync():
    result = t1.apply_async(args=[5, 10], kwargs={"message": "The sum is"})
    task_result = result.get()
    print("Task is running synchronously")
    print(task_result)


# Asynchronous task execution
def execute_async():
    result = t1.apply_async(args=[5, 10], kwargs={"message": "The sum is"})
    print("Task is running asynchronously")
    print("Task ID:", result.task_id)
