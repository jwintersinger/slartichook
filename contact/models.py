from appengine_django.models import BaseModel
from google.appengine.ext import db

class Missive(BaseModel):
  name       = db.StringProperty(required=True)
  email      = db.EmailProperty(required=True)
  message    = db.TextProperty(required=True)
  created_at = db.DateTimeProperty(required=True, auto_now_add=True)
