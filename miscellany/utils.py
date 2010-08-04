from django import template
def render_email(subject_template_name, message_template_name, **kwargs):
  subject_template = template.loader.get_template(subject_template_name)
  message_template = template.loader.get_template(message_template_name)
  context = template.Context(kwargs)
  return (subject_template.render(context).strip(),
          message_template.render(context))
