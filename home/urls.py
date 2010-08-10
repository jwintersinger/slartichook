from django.conf.urls.defaults import *

urlpatterns = patterns('home.views',
  url(r'^$', 'home', name='home'),
)
