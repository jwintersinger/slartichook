from django.views.generic.simple import direct_to_template
from work.models import Project
from contact.forms import ContactForm

def home(request):
  return direct_to_template(request, 'home/home.html', {
    'project_list': Project.all(),
    'contact_form': ContactForm(),
  })
