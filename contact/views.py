from django.views.generic.simple import direct_to_template
from google.appengine.api.mail import send_mail
from miscellany.utils import render_email
from settings import CONTACT_TO
from contact.forms import ContactForm
from contact.models import Missive

def contact(request):
  if request.method != 'POST':
    raise Exception('Request type is not POST')
  contact_form = ContactForm(request.POST)

  if contact_form.is_valid():
    form_data = contact_form.cleaned_data
    _send_contact_email(form_data)
    _store_contact(form_data)
    return direct_to_template(request, 'contact/_success.html')
  return direct_to_template(request, 'contact/_form.html',
    {'contact_form': contact_form})

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
