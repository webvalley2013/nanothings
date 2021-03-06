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
from django.conf.urls import patterns, url

urlpatterns = patterns('userinterface.views',

    url(r'^$', 'home', name='home'),
    url(r'about/$', 'about'),
    url(r'download/$', 'download'),
    url(r'api_documentation/$', 'api_doc'),
    url(r'license/$', 'license'),

    url(r'run/(\d+)/$', 'run_process', name='run_process_gui'),

    #ADMIN PROCESS AREA
    url(r'uiprocess_list/$', "list_of_processes"),
    url(r'uiprocess/(\d+)/$', 'detail'),
    url(r'ui/process/abort/(\d+)/$', 'abort'),
    url(r'celery_error/$', 'celery_error'),

)
