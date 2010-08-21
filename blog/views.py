from django.core import paginator, urlresolvers
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from blog.models import Post

def post_list(request, page=None):
  #_create_test_post()
  posts = Post.all()
  posts.order('-created_at')

  if not page:
    page = 1
  pgnr = paginator.Paginator(posts, 3)
  try:
    paginated_posts = pgnr.page(page)
  except (paginator.EmptyPage, paginator.InvalidPage):
    return HttpResponseRedirect(urlresolvers.reverse('blog.views.post_list'))

  return direct_to_template(request, 'blog/post_list.html', {
    'paginated_posts': paginated_posts,
  })

def _create_test_post():
  from google.appengine.ext import db
  from django.contrib.webdesign import lorem_ipsum
  from datetime import datetime
  p = Post(
    title = 'Happy happy',
    body = (2*'\n').join(lorem_ipsum.paragraphs(4)),
    #user = users.get_current_user(),
    tags = [db.Category('bonners'), db.Category('cheese'), db.Category('weiners')],
    slug = 'phallus',
    created_at = datetime.fromtimestamp(1282380470 - 365*24*60*60),
  )
  p.put()

def post_detail(request, slug):
  post = Post.objects.all()
  post.filter('slug =', slug)
  return direct_to_template(request, 'blog/post_detail.html', {
    'post': post.fetch(1)[0],
  })

def post_archive(request, tag=None):
  posts = Post.objects.all()
  posts.order('-created_at')
  if tag:
    posts.filter('tags =', tag)

  return direct_to_template(request, 'blog/post_archive.html', {
    'posts': posts,
    'tag':   tag
  })
