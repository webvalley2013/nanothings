from django.conf.urls import patterns, url
from process import views

urlpatterns = patterns('process.views',
    url(r'^list/$', 'process_list'),
    url(r'run/process_test/(\d+)/(\d+)$', 'run_process_test'),
    url(r'run/process_get$', 'run_process_get'),
    url(r'run/process_post$', 'run_process_post'),
    url(r'run/process/3d/(\d+)$', 'run_process_3d', name='run3d'),
    url(r'status/(\d+)$', 'status', name="status"),
    url(r'detail/(\d+)$', 'detail', name="detail"),
)

