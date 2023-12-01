from __future__ import annotations

from typing import Any

from django import template
from django.db.models import QuerySet
from wagtail.models import Page, Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_menu_items(context: Any) -> QuerySet[Page]:
    root_page = Site.find_for_request(context["request"]).root_page
    return root_page.get_children().live().in_menu()
