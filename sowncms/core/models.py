from django.conf import settings
from django.db import models

from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.contrib.settings.models import (
    BaseSiteSetting,
    register_setting,
)

@register_setting
class SiteSettings(BaseSiteSetting):

    brand = models.CharField(max_length=15, choices=settings.AVAILABLE_BRANDS, default="sown")
    discord_invite = models.URLField(blank=True, null=True)
    github_org = models.CharField(blank=True, null=True, max_length=63, verbose_name="GitHub Username / Org Name")

    class Meta:
        verbose_name = "Site Settings"

    panels = [
        FieldPanel("brand"),
        MultiFieldPanel([
            FieldPanel("discord_invite"),
            FieldPanel("github_org"),
        ], heading="Social Media")
    ]
