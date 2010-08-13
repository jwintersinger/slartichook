from django.views.generic.simple import direct_to_template
from home.models import Work
from contact.forms import ContactForm

def home(request):
  return direct_to_template(request, 'home/home.html', {
    'project_list': Work.projects(),
    'contact_form': ContactForm(),
  })
