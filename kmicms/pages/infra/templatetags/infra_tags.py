from __future__ import annotations

from django import template

register = template.Library()


@register.filter(name="format_dns")
def format_dns(value: str, default_domain: str = "sown.org.uk") -> str:
    if "." in value:
        return value
    else:
        return f"{value}.{default_domain}"
