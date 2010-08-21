from datetime import datetime
from appengine_django.models import BaseModel
from google.appengine.ext import db
from django.core import urlresolvers

class Post(BaseModel):
  user         = db.UserProperty(required=False, auto_current_user_add=True)
  title        = db.StringProperty(required=True)
  body         = db.TextProperty(required=True)
  published_at = db.DateTimeProperty(required=True, auto_now_add=True)
  created_at   = db.DateTimeProperty(required=True, auto_now_add=True)
  updated_at   = db.DateTimeProperty(required=True, auto_now=True)
  tags         = db.ListProperty(db.Category)
  slug         = db.StringProperty(required=True)

  @classmethod
  def visible(cls):
    posts = cls.all()
    posts.filter('published_at <=', datetime.utcnow())
    posts.order('-published_at')
    return posts

  def get_absolute_url(self):
    return urlresolvers.reverse('blog.views.post_detail', kwargs={
      'slug': self.slug
    })

  def put(self):
    if not self._is_slug_unique(self.slug):
      raise SlugNotUniqueException('Slug "%s" is not unique' % self.slug)
    return super(Post, self).put()

  def _is_slug_unique(self, slug):
    posts = Post.objects.all()
    posts.filter('slug =', slug)
    return posts.count(1) == 0


class SlugNotUniqueException(Exception):
  pass
