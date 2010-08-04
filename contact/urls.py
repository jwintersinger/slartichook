from django.conf.urls.defaults import *

urlpatterns = patterns('contact.views',
  url(r'^$', 'contact', name='contact-home'),
  url(r'^confirmation/$', 'contact_confirmation'),
)
