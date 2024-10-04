from django import template
from django.core.cache import cache  # noqa: F401

register = template.Library()


@register.simple_tag(takes_context=True)
def is_premium_user(context):
    request = context["request"]
    if not request.user.is_authenticated:
        return False
    # cache_key = f"{request.user.id}_is_premium"  # noqa: ERA001
    # is_premium = cache.get(cache_key)  # noqa: ERA001
    return request.user.groups.filter(name="Premium").exists()
