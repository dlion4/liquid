from django import template

register = template.Library()


@register.filter(name="format_phone_number")
def format_phone_number(value):
    """Formats the phone number to add a leading zero if less than 10."""
    return f"{value}" if str(value).startswith("7") else value
