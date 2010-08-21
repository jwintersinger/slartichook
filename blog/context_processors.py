from blog.models import Post

def recent_posts(request):
  return {
    'recent_posts': Post.all().fetch(5),
  }
