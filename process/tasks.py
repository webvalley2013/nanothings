from celery import task
from .extralib.imageanalisys import main2d


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


@task()
def run_3d_analisys(n1,n2,l1,l2,outpath):
    main2d.main(n1,n2,l1,l2,outpath)
    return outpath





