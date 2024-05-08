from django import template

register = template.Library()


@register.filter(name="format_indexed_count")
def format_indexed_count(value):
    """Formats the plans count to add a leading zero if less than 10."""
    return f"0{value}" if value < 10 else value
