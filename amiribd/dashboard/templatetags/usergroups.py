from django import template
from django.core.cache import cache

register = template.Library()


@register.simple_tag(takes_context=True)
def is_premium_user(context):
    request = context["request"]
    if not request.user.is_authenticated:
        return False

    # cache_key = f"{request.user.id}_is_premium"
    # is_premium = cache.get(cache_key)

    is_premium = request.user.groups.filter(name="Premium").exists()
    print(is_premium)
    return is_premium
