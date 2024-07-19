from django import template

register = template.Library()

@register.filter(name='endswith_ext')
def endswith_ext(value, extension):
    return value.endswith(extension)

