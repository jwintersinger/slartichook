from django.shortcuts import render_to_response
from home.models import Work

def home(request):
  return render_to_response('home/home.html', {
    'project_list': Work.projects()
  })
