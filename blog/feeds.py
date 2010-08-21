from django.core import urlresolvers
from django.contrib.syndication.views import Feed
from blog.models import Post

class LatestPosts(Feed):
  title                = 'Giant phallus'
  link                 = urlresolvers.reverse('blog-home')
  description          = 'Latests posts from giant phallus.'
  title_template       = 'feeds/blog_post_title.html'
  description_template = 'feeds/blog_post_description.html'

  def items(self):
    return Post.visible().fetch(15)

  def item_pubdate(self, post):
    return post.published_at

