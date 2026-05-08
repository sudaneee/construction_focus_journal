from django import template

register = template.Library()


@register.filter
def ordinal(value):
    try:
        n = int(value)
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"
    except (TypeError, ValueError):
        return value
