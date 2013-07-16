from django.conf.urls import patterns

urlpatterns = patterns('userinterface.views',
    (r'process_list/$', "list_of_processes"),
    (r'process/(\d+)/$', 'detail'),
    (r'process/abort/(\d+)/$', 'abort'),
    (r'^$', 'home'),
    (r'^about/$', 'about'),
    (r'^contacts/$', 'contacts'),
    (r'^img_analysis/$', 'img_analysis'),
    (r'^r_plr/$', 'r_plr'),
    (r'^networks/$', 'networks'),
)
