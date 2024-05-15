from django import template

register = template.Library()


@register.filter(name="whatsapp_earnings")
def whatsapp_earnings(value):
    # Assuming 'value' is a dictionary where 'WhatsApp' earnings can be accessed
    # Adjust the logic based on your actual data structure
    return value.get("WhatsApp", 0.00)
