# MODULES
from celery import task
from .extralib.imageanalisys import main2d
from nanothings.settings import DEFAULT_HTTP_OUTPUT


@task()
def add(x, y):
    import time
    time.sleep(600)
    return x + y


@task()
def process_int(x, y, tsleep):
    import time
    time.sleep(tsleep)
    return x * y


@task()
def minus(x, y):
    import time
    time.sleep(15)
    return x - y


@task()
def run_3d_analisys(n1, n2, l1, l2, outpath):
    main2d.main(n1, n2, l1, l2, outpath)
    return DEFAULT_HTTP_OUTPUT + outpath





