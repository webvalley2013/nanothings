from django.conf.urls import patterns, url
import process.views

urlpatterns = patterns('process.views',
    (r'list/$', 'process_list'),
    (r'run/process_test/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/3danlysis/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/plrfunc/(\d+)/(\d+)/$', 'run_process_test'),
#   (r'run/hadoop/(\d+)/(\d+)/$', 'run_process_test'),
    (r'status/(\d+)/$', 'status'),

)

urlpatterns = patterns('',
    url(r'^list/$', views.process_list,  name="process_list"),
    url(r'^analyse/index.html',     views.index, name="index"),
)
