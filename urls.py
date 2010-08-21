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

    url(r'^feeds/posts/$', 'blog.views.latest_posts', name='blog-posts-feed'),

    # If the equivalent line is in home/urls.py, reverse-matching the route via
    # "{% url home %} in a template results in an empty string being returned.
    # To get the desired "/", the route must be here instead.
    url(r'^$',        'home.views.home', name='home'),
    # For some reason, placing the equivalent line in home/urls.py results in
    # the route never being matched, so instead of using home/urls.py, I place
    # it here instead.
    url(r'^clear/$',  'home.views.clear_cache'),
)
