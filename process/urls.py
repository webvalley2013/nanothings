from django.conf.urls import patterns, url
from process import views

urlpatterns = patterns('process.views',
    (r'^list/$', 'process_list'),
    (r'run/process_test/(\d+)/(\d+)/$', 'run_process_test'),
    (r'run/process_get/$', 'run_process_get'),
    (r'run/process_post/$', 'run_process_post'),
#   (r'run/3danlysis/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/plrfunc/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/hadoop/(\d+)/(\d+)/$', 'run_process_test'),



    url(r"status/(\d+)", views.status, name="status"),
    url(r"detail/(\d+)$", views.detail, name="detail"),
)

