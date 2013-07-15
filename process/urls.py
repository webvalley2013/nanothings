from django.conf.urls import patterns

urlpatterns = patterns('process.views',
    (r'list/$', 'process_list'),
    (r'run/process_test/(\d+)/(\d+)/$', 'run_process_test'),
    (r'run/process_get/$', 'run_process_get'),
    (r'run/process_post/$', 'run_process_post'),
#   (r'run/3danlysis/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/plrfunc/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/hadoop/(\d+)/(\d+)/$', 'run_process_test'),
#    (r'status/(\d+)/$', 'status'),
)
