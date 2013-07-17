# This file is part of nanothings.
#
#     nanothings is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero GPL as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     nanothings is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero GPL for more details.
#
#     You should have received a copy of the GNU Affero GPL
#     along with nanothings.  If not, see <http://www.gnu.org/licenses/>.

# MODULES
from django.conf.urls import patterns, url

urlpatterns = patterns('process.views',
    url(r'^list/$', 'process_list'),
    url(r'run/test_int/(\d+)$', 'run_test_int'),
    url(r'run/process/3d/(\d+)$', 'run_process_3d', name='run3d'),
    url(r'status/(\d+)$', 'status', name="status"),
    url(r'detail/(\d+)$', 'detail', name="detail"),
    #  (r'run/plrfunc/(\d+)/(\d+)/$', 'run_process_test'),
    #  (r'run/hadoop/(\d+)/(\d+)/$', 'run_process_test'),
)

