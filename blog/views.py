from django.core import paginator, urlresolvers
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from blog.models import Post

def post_list(request, page=None):
  #_create_test_posts()
  posts = Post.visible()

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

def post_detail(request, slug):
  post = Post.visible()
  post.filter('slug =', slug)
  return direct_to_template(request, 'blog/post_detail.html', {
    'post': post.fetch(1)[0],
  })

def post_archive(request, tag=None):
  posts = Post.visible()
  if tag:
    posts.filter('tags =', tag)
  return direct_to_template(request, 'blog/post_archive.html', {
    'posts': posts,
    'tag':   tag
  })

def _create_test_post(slug, time_delta):
  from google.appengine.ext import db
  from django.contrib.webdesign import lorem_ipsum
  from datetime import datetime
  p = Post(
    title         = 'Happy happy',
    body          = (2*'\n').join(lorem_ipsum.paragraphs(4)),
    #user          = users.get_current_user(),
    tags          = [
      db.Category('bonners'),
      db.Category('cheese'),
      db.Category('weiners')
    ],
    slug          = slug,
    published_at = datetime.fromtimestamp(1282380470 - time_delta),
  )
  p.put()

def _create_test_posts():
  _create_test_post('phallus', 365*24*60*60)
  _create_test_post('weiner', 180*24*60*60)
  _create_test_post('peanut_butter', 5*60)
