from django.db import models
from wagtail.contrib.settings.models import (
    BaseSiteSetting,
    register_setting,
)

@register_setting
class SocialMediaSettings(BaseSiteSetting):

    discord_invite = models.URLField(blank=True, null=True)
    github_org = models.CharField(blank=True, null=True, max_length=63, verbose_name="GitHub Username / Org Name")
    class Meta:
        verbose_name = "Social Media Settings"