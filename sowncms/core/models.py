from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField

from core.blocks.nav import FooterMenuBlock, MainMenuBlock
from core.utils import last_year, max_value_current_year


@register_setting
class SiteSettings(BaseSiteSetting):

    title = models.CharField(max_length=63, blank=True, help_text="This is used in the footer")
    brand = models.CharField(max_length=15, choices=settings.AVAILABLE_BRANDS, default="sown")
    copyright_start_year = models.PositiveIntegerField(
        default=last_year,
        validators=[MinValueValidator(1950), max_value_current_year],
        help_text='The initial year of copyright for the site.',
    )

    main_menu = StreamField(MainMenuBlock(), blank=True, use_json_field=True)
    footer_menu = StreamField(FooterMenuBlock(), blank=True, use_json_field=True)

    discord_invite = models.URLField(blank=True)
    github_org = models.CharField(blank=True, max_length=63, verbose_name="GitHub Username / Org Name")

    class Meta:
        verbose_name = "Site Settings"

    branding_panels = [
        FieldPanel('title'),
        FieldPanel('brand'),
        FieldPanel('copyright_start_year'),
    ]

    navigation_panels = [
        FieldPanel('main_menu'),
        FieldPanel('footer_menu'),
    ]

    social_media_panels = [
        FieldPanel('discord_invite'),
        FieldPanel('github_org'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(branding_panels, heading='Branding'),
        ObjectList(navigation_panels, heading='Navigation'),
        ObjectList(social_media_panels, heading='Social Media'),
    ])
