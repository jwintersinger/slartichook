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

def post_detail(request):
  pass

def post_archive(request):
  pass
