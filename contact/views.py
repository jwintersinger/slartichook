from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from google.appengine.api.mail import send_mail
from miscellany.utils import render_email
from settings import CONTACT_TO
from contact.forms import ContactForm
from contact.models import Missive

def contact(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      _send_contact_email(form_data)
      _store_contact(form_data)
      return HttpResponseRedirect(reverse('contact.views.contact_confirmation'))
  else:
    form = ContactForm()
  return render_to_response('contact/form.html', {'form': form})

def contact_confirmation(request):
  return render_to_response('contact/confirmation.html')

def _send_contact_email(form_data):
  subject, message = render_email(
    'contact/email_subject.html',
    'contact/email_message.html',
    message      = form_data['message'],
    from_name    = form_data['name'],
    from_address = form_data['email']
  )
  # BUG: with appengine_django, one should be able to use
  # django.core.mail.send_mail. This only works for Django 1.1, however --
  # Django 1.2 throws a variety of exceptions, as appengine_django hasn't
  # been properly updated for Django 1.2's mail code. Thus, I must use the
  # native mail API built into App Engine.
  return send_mail(form_data['email'], CONTACT_TO, subject, message)

# Store contact on the off-chance that something goes awry with the e-mail
# sending process.
def _store_contact(form_data):
  missive = Missive(
    name    = form_data['name'],
    email   = form_data['email'],
    message = form_data['message']
  )
  return missive.put()
