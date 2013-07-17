from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # App urls
    url(r'^process/', include('process.urls')),
    url(r'^ui/', include('userinterface.urls')),

    # Login and logout urls
    (r'^accounts/login/$', 'userinterface.views.login_view'),
    (r'^accounts/logout/$', 'userinterface.views.logout_view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
