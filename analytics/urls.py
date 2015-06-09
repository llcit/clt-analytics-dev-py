from django.conf.urls import patterns, include, url
from django.template import RequestContext

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Apps
    url(r'^review/', include('review.urls'), name='review'),
    url(r'^analytics/', 'analytics.views.index', name='index'),
    url(r'^$', 'analytics.views.index'),

    # include to use the django framework login views
     url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    # include to use the framework logout views
     url(r'^logout/', 'django.contrib.auth.views.logout'),

    url(r'^login-select/', 'analytics.views.login_select', name='login-select'),

    # Guest/Non-UH user
    url(r'^guest/login/', 'analytics.views.local_login', name="local-login"),

    #Use the following for UH Auth
    # url(r'^accounts/login/$', 'django_cas.views.login'),
    # url(r'^logout/$', 'django_cas.views.logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)