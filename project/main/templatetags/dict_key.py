from django import template

register = template.Library()

@register.filter
def dict_key(value, key):
    try:
        return value[key]
    except KeyError:
        return ''