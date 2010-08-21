from blog.models import Post

def recent_posts(request):
  recent_posts = Post.all()
  recent_posts.order('-created_at')
  return {
    'recent_posts': recent_posts.fetch(5),
  }
