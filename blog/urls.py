from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
  url(r'^$',                             'post_list',    name='blog-home'),
  url(r'^(?P<page>\d+)/$',               'post_list'),
  url(r'^archive/$',                     'post_archive', name='blog-archive'),
  url(r'^archive/(?P<tag>[\w -]+)/$',    'post_archive'),
  url(r'^(?P<slug>[\w-]+)/$',            'post_detail'),
)
