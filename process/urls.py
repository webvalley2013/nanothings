# MODULES
from django.conf.urls import patterns, url
from process import views

urlpatterns = patterns('process.views',
    url(r'^list/$', 'process_list'),
    url(r'run/test_int/(\d+)$', 'run_test_int'),
    url(r'run/process/3d/(\d+)$', 'run_process_3d', name='run3d'),
    url(r'status/(\d+)$', 'status', name="status"),
    url(r'detail/(\d+)$', 'detail', name="detail"),
    #  (r'run/plrfunc/(\d+)/(\d+)/$', 'run_process_test'),
    #  (r'run/hadoop/(\d+)/(\d+)/$', 'run_process_test'),
)

