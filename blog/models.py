from appengine_django.models import BaseModel
from google.appengine.ext import db
from django.core import urlresolvers

class Post(BaseModel):
  user       = db.UserProperty(required=False, auto_current_user_add=True)
  title      = db.StringProperty(required=True)
  body       = db.TextProperty(required=True)
  created_at = db.DateTimeProperty(required=True, auto_now_add=True)
  updated_at = db.DateTimeProperty(required=True, auto_now=True)
  tags       = db.ListProperty(db.Category)
  slug       = db.StringProperty(required=True)

  def get_absolute_url(self):
    return urlresolvers.reverse('blog.views.post_detail', kwargs={
      'slug': self.slug
    })
