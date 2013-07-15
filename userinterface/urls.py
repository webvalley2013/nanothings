from django.conf.urls import patterns, url
from userinterface import views

urlpatterns = patterns("",
    url(r'process_list/$', views.list_of_processes, name="list_of_processes"),
    url(r'process/(\d+)/$', views.detail, name="detail"),
    url(r'^',  views.home, name="index"),
)
