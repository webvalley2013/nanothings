# This file is part of nanothings.
#
#     nanothings is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero GPL as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero GPL for more details.
#
#     You should have received a copy of the GNU Affero GPL
#     along with nanothings.  If not, see <http://www.gnu.org/licenses/>.
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





