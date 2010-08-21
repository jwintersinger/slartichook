import settings
from django.core import urlresolvers
from django.contrib.syndication.views import Feed
from blog.models import Post

class LatestPosts(Feed):
  title                = settings.SITE_NAME
  link                 = urlresolvers.reverse('blog-home')
  description          = 'Latests posts from %s' % settings.SITE_NAME
  title_template       = 'feeds/blog_post_title.html'
  description_template = 'feeds/blog_post_description.html'

  def items(self):
    return Post.visible().fetch(15)

  def item_pubdate(self, post):
    return post.published_at

