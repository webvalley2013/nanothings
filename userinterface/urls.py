from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'process_list/$', views.list_of_processes, name="list_of_processes"),
    url(r'process/(\d+)/$', views.detail, name="detail"),
    #url(r'abort/process/(\d+)/$', views.abort, name="abort"),
    url(r'process/abort/(\d+)/$', views.abort, name="abort"),
    url(r'^$',  views.home, name="index"),
)
