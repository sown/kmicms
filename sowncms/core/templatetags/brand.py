from urllib.parse import quote, urljoin

from django import template
from django.apps import apps
from django.templatetags.static import PrefixNode
from django.utils.html import conditional_escape

from core.models import SiteSettings

register = template.Library()

class StaticNode(template.Node):
    child_nodelists = ()

    def __init__(self, varname=None, path=None):
        if path is None:
            raise template.TemplateSyntaxError(
                "Static template nodes must be given a path to return."
            )
        self.path = path
        self.varname = varname

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(varname={self.varname!r}, path={self.path!r})"
        )

    def url(self, context):
        path = self.path.resolve(context)
        site_settings = SiteSettings.for_request(context["request"])
        path = urljoin(f'brands/{site_settings.brand}/', path)
        return self.handle_simple(path)

    def render(self, context):
        url = self.url(context)
        if context.autoescape:
            url = conditional_escape(url)
        if self.varname is None:
            return url
        context[self.varname] = url
        return ""

    @classmethod
    def handle_simple(cls, path):
        if apps.is_installed("django.contrib.staticfiles"):
            from django.contrib.staticfiles.storage import staticfiles_storage

            return staticfiles_storage.url(path)
        else:
            return urljoin(PrefixNode.handle_simple("STATIC_URL"), quote(path))

    @classmethod
    def handle_token(cls, parser, token):
        """
        Class method to parse prefix node and return a Node.
        """
        bits = token.split_contents()

        if len(bits) < 2:
            raise template.TemplateSyntaxError(
                "'%s' takes at least one argument (path to file)" % bits[0]
            )

        path = parser.compile_filter(bits[1])

        if len(bits) >= 2 and bits[-2] == "as":
            varname = bits[3]
        else:
            varname = None

        return cls(varname, path)


@register.tag
def static_for_brand(parser, token):
    """
    Join the given path with the STATIC_URL directory for the brand.

    Usage::

        {% static path [as varname] %}

    Examples::

        {% static_for_brand "myapp/css/base.css" %}
        {% static_for_brand variable_with_path %}
        {% static_for_brand "myapp/css/base.css" as admin_base_css %}
        {% static_for_brand variable_with_path as varname %}
    """
    return StaticNode.handle_token(parser, token)