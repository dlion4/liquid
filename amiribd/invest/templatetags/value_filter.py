from django import template
import re

register = template.Library()


@register.filter(name="strip_none")
def strip_filter(value):
    """Removes 'None' from the start of the string and returns the rest."""
    return re.sub(r"^None", "", value)



@register.filter
def last_three_digits(value):
    """Returns the last three digits of the phone number."""
    return str(value)[-3:]