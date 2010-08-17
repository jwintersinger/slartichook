import settings

# A simpler approach to including Analytics would be to include an external
# Javascript file from within the template only if settings.DEBUG is set to
# False. The problem with this method is that
# django.core.context_processors.debug only sets the "debug" context variable
# to True if settings.DEBUG is True, *and* if the user's IP is in
# settings.INTERNAL_IPS. Furthermore, it means that the Google Analytics
# account name is hardcoded in that external Javascript file.

# By relying on a custom context processor, we ensure that the Analytics code
# will never be included when in DEBUG mode, even if settings.INTERNAL_IPS is
# unset, and we allow the user to specify his Analytics account in
# settings_deployment.py.
def google_analytics(request):
  try:
    return {'google_analytics_account': settings.GOOGLE_ANALYTICS_ACCOUNT}
  except AttributeError:
    return {}
