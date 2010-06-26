from django.core import paginator, urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from blog.models import Post

def post_list(request, page=None):
  #_create_test_post()
  posts = Post.objects.all()
  posts.order('-created_at')

  if not page:
    page = 1
  pgnr = paginator.Paginator(posts, 3)
  try:
    paginated_posts = pgnr.page(page)
  except (paginator.EmptyPage, paginator.InvalidPage):
    return HttpResponseRedirect(urlresolvers.reverse('blog.views.post_list'))

  return render_to_response('blog/post_list.html', {'posts': paginated_posts})

def _create_test_post():
  from google.appengine.ext import db
  p = Post(
    title = 'Happy happy',
    body = 'Socks.\n\n* Whoa\n* Yeah',
    #user = users.get_current_user(),
    tags = [db.Category('bonners'), db.Category('cheese'), db.Category('weiners')],
    slug = 'phallus',
  )
  p.put()

def post_detail(request, slug):
  post = Post.objects.all()
  post.filter('slug =', slug)
  return render_to_response('blog/post_detail.html', {'post': post.fetch(1)[0]})

def post_archive(request, tag=None):
  posts = Post.objects.all()
  posts.order('-created_at')
  if tag:
    posts.filter('tags =', tag)

  return render_to_response('blog/post_archive.html', {
    'posts': posts,
    'tag':   tag
  })
