from celery import task

@task()
def add(x, y):
    import time
    time.sleep(5)
    return x + y