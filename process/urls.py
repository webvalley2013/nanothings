from django.conf.urls import patterns, url
from process import views

urlpatterns = patterns('process.views',
     url(r'^list/$', views.process_list,  name="process_list"),
     url(r"run/process_test/(\d+)/(\d+)/$", views.run_process_test, name="run_process_test"),
     (r'run/process_get/$', 'run_process_get'),
     (r'run/process_post/$', 'run_process_post'),
#   (r'run/3danlysis/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/plrfunc/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/hadoop/(\d+)/(\d+)/$', 'run_process_test'),


    url(r"status/(\d+)", views.status, name="status"),
)

