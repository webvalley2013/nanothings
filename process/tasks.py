from celery import task

@task()
def add(x, y):
    import time
    time.sleep(600)
    return x + y

@task()
def multiply(x, y):
    import time
    time.sleep(15)
    return x * y

@task()
def minus(x, y):
    import time
    time.sleep(15)
    return x - y
