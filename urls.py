from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^slartichook/', include('slartichook.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^blog/',    include('blog.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^$',        include('home.urls')),
    # For some reason, placing the equivalent line in home/urls.py results in
    # the route never being matched, so I place it here instead.
    url(r'^clear/$',  'home.views.clear_cache'),
)
