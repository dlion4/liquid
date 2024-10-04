from django import template

register = template.Library()

INDEXED_COUNT=10


@register.filter(name="format_indexed_count")
def format_indexed_count(value):
    """Formats the plans count to add a leading zero if less than 10."""
    return f"0{value}" if value < INDEXED_COUNT else value
