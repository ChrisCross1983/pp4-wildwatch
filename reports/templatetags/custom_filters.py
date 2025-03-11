from django import template

register = template.Library()


@register.filter
def force_https(value):
    if isinstance(value, str):
        return value.replace("http://", "https://")
    return value
