from django.views.generic.simple import direct_to_template
from work.models import Project
from contact.forms import ContactForm
from django.views.decorators.cache import cache_page

@cache_page(24*60*60) # Cache for one day.
def home(request):
  return direct_to_template(request, 'home/home.html', {
    'project_list': Project.all(),
    'contact_form': ContactForm(),
  })

# Unauthenticated users can clear cache, but generating the cached page is not
# terribly expensive, so I'm not worried.
def clear_cache(request):
  from django.core.cache import cache
  from django.http import HttpResponse
  cache.clear()
  return HttpResponse('Cache cleared.')
