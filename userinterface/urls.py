from django.conf.urls import patterns, url

urlpatterns = patterns('userinterface.views',
    url(r'process_list/$', "list_of_processes"),
    url(r'process/(\d+)/$', 'detail'),
    url(r'process/abort/(\d+)/$', 'abort'),
    url(r'celery_error/$', 'celery_error'),

    url(r'^$', 'home', name='home'),
    url(r'^about/$', 'about'),
    url(r'^contacts/$', 'contacts'),
    url(r'^api_documentation/$', 'api_doc'),
    url(r'^license/$', 'license'),
    url(r'^img_analysis/$', 'img_analysis'),
    url(r'^r_plr/$', 'r_plr'),
    url(r'^networks/$', 'networks'),
)
