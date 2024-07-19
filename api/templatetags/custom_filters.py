from django import template

register = template.Library()

@register.filter
def get_file_type(file_name):
    if file_name.endswith('.pdf'):
        return 'pdf'
    elif file_name.endswith('.doc') or file_name.endswith('.docx'):
        return 'doc'
    elif file_name.endswith('.ppt') or file_name.endswith('.pptx'):
        return 'ppt'
    else:
        return 'other'