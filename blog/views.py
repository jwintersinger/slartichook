from django.http import HttpResponse
from django.shortcuts import render_to_response
from blog.models import Post
from google.appengine.ext import db

def post_list(request):
  p = Post(
    title = 'Happy happy',
    body = 'Socks.',
    #user = users.get_current_user(),
    tags = [db.Category('happiness')],
    slug = 'slug',
  )
  p.put()

  return render_to_response('blog/post_list.html', {'posts': Post.objects.all()})

def post_detail(request, slug):
  post = Post.objects.all()
  post.filter('slug =', slug)
  return render_to_response('blog/post_detail.html', {'post': post.fetch(1)[0]})

def post_archive(request):
  return render_to_response('blog/post_archive.html', {'posts': Post.objects.all()})
