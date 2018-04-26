from django.conf.urls import include, url
from django.template import RequestContext

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import analytics.views
import django_cas_ng.views

urlpatterns = [
    # Apps
    url(r'^review/', include('review.urls')),
    url(r'^analytics/', analytics.views.index, name='index'),
    url(r'^$', analytics.views.index),

    # Guest/Non-UH login form
    url(r'^login/', analytics.views.local_login, name='login-screen'),

    # Guest/Non-UH user login handler
    url(r'^guest/login/', analytics.views.local_login_handler, name="local-login"),

    #Use the following for UH Auth
    url(r'^accounts/login/$', django_cas_ng.views.login, name='remote-login'),
    url(r'^logout/$', django_cas_ng.views.logout, name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
