from django.views.generic.simple import direct_to_template
from google.appengine.api import mail
from google.appengine.ext import db
from miscellany.utils import render_email
from settings import CONTACT
from contact.forms import ContactForm
from contact.models import Missive

def contact(request):
  if request.method != 'POST':
    raise Exception('Request type is not POST')
  contact_form = ContactForm(request.POST)

  if contact_form.is_valid():
    form_data = contact_form.cleaned_data
    if _send_contact_email(form_data) and _store_contact(form_data):
      return direct_to_template(request, 'contact/_success.html')
  return direct_to_template(request, 'contact/_form.html',
    {'contact_form': contact_form, 'error_occurred': True})

def _send_contact_email(form_data):
  subject, message = render_email(
    'contact/email_subject.html',
    'contact/email_message.html',
    message      = form_data['message'],
    from_name    = form_data['name'],
    from_address = form_data['email'],
  )
  # BUG: with appengine_django, one should be able to use
  # django.core.mail.send_mail. This only works for Django 1.1, however --
  # Django 1.2 throws a variety of exceptions, as appengine_django hasn't
  # been properly updated for Django 1.2's mail code. Thus, I must use the
  # native mail API built into App Engine.
  try:
    mail.send_mail(CONTACT['from'], CONTACT['to'], subject, message)
    return True
  except mail.Error:
    return False

# Store contact on the off-chance that something goes awry with the e-mail
# sending process.
def _store_contact(form_data):
  missive = Missive(
    name    = form_data['name'],
    email   = form_data['email'],
    message = form_data['message']
  )
  try:
    missive.put()
    return True
  except db.Error:
    return False
