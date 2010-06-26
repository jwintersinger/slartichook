from django import template
import datetime

register = template.Library()

@register.filter
def int_to_month_name(month_int):
  return datetime.date(2000, month_int, 1).strftime('%B')
