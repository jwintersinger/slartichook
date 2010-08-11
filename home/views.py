from django.views.generic.simple import direct_to_template
from home.models import Work

def home(request):
  return direct_to_template(request, 'home/home.html', {
    'project_list': Work.projects()
  })
