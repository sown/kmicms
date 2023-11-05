from django import template
from wagtail.models import Site


register = template.Library()


@register.simple_tag(takes_context=True)
def get_menu_items(context):
    root_page = Site.find_for_request(context["request"]).root_page
    return root_page.get_children().live().in_menu()
