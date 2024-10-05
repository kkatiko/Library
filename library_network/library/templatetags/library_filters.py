from django import template
from library.models import Library

register = template.Library()

@register.filter(name='get_library')
def get_library(libraries, library_id):
    try:
        return libraries.get(id=library_id).name
    except Library.DoesNotExist:
        return 'Unknown Library'
