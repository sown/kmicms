from typing import Any
from urllib.parse import urljoin

from django import template
from django.templatetags.static import StaticNode

from core.models import SiteSettings

register = template.Library()


class BrandStaticNode(StaticNode):
    def url(self, context: Any) -> str:
        path = self.path.resolve(context)
        site_settings = SiteSettings.for_request(context["request"])
        path = urljoin(f"brands/{site_settings.brand}/", path)
        return self.handle_simple(path)


@register.tag
def static_for_brand(parser: Any, token: Any) -> str:
    """
    Join the given path with the STATIC_URL directory for the brand.

    Usage::

        {% static_for_brand path [as varname] %}

    Examples::

        {% static_for_brand "myapp/css/base.css" %}
        {% static_for_brand variable_with_path %}
        {% static_for_brand "myapp/css/base.css" as admin_base_css %}
        {% static_for_brand variable_with_path as varname %}
    """
    return BrandStaticNode.handle_token(parser, token)
