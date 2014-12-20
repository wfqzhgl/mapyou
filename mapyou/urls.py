from django.conf.urls import patterns, include, url

from django.contrib import admin

from app.views import *
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'mapyou.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       (r'^accounts/login/$', login_custom),
                       (r'^accounts/logout/$', login_required(logout_custom)),
                       (r'^accounts/password_change/$', login_required(password_change)),
                       # (r'^$', login_custom),
                       (r'^$', index),
                       url(r'^app/', include('app.urls', namespace='app')),
)
