from django import template

register = template.Library()

@register.filter
def is_pdf(value):
    return value.endswith('.pdf')

@register.filter
def is_doc(value):
    return value.endswith('.doc') or value.endswith('.docx')

@register.filter
def is_ppt(value):
    return value.endswith('.ppt') or value.endswith('.pptx')