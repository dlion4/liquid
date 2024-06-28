from django import template


register = template.Library()

@register.filter(name='filter_h2_template')
def filter_h2_template(value):
    # first_h2_html_tag = value.find("<h2>")
    # last_h2_html_tag = value.find("</h2>")
    last_h2_html_tag = value.find("</h2>")

    return value[last_h2_html_tag+8:]
    # return value[first_h2_html_tag+4:last_h2_html_tag]