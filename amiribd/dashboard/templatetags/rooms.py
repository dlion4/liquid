from django import template


register = template.Library()


@register.filter(name="generate_initials")
def generate_initials(value):
    """Generates the initials of a given name. If the name has multiple parts, it returns the first letter of the first and last parts. If it's a single name, it returns the first two letters."""
    parts = value.split()
    if len(parts) > 1:
        return parts[0][0] + parts[-1][0]
    else:
        return parts[0][:2] if len(parts[0]) > 1 else parts[0]
