from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
                       url(r'^home[/]?', 'index', name='index'),

)