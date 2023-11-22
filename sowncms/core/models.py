from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import Orderable

from core.blocks.nav import FooterMenuBlock, MainMenuBlock
from core.utils import get_social_media_service_choices, get_social_media_services, last_year, max_value_current_year


@register_setting
class SiteSettings(ClusterableModel, BaseSiteSetting):

    title = models.CharField(max_length=63, blank=True, help_text="This is used in the footer")
    brand = models.CharField(max_length=15, choices=settings.AVAILABLE_BRANDS, default="sown")
    copyright_start_year = models.PositiveIntegerField(
        default=last_year,
        validators=[MinValueValidator(1950), max_value_current_year],
        help_text='The initial year of copyright for the site.',
    )

    main_menu = StreamField(MainMenuBlock(), blank=True, use_json_field=True)
    footer_menu = StreamField(FooterMenuBlock(), blank=True, use_json_field=True)

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
        InlinePanel('social_media_accounts', heading="Social Media Accounts"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(branding_panels, heading='Branding'),
        ObjectList(navigation_panels, heading='Navigation'),
        ObjectList(social_media_panels, heading='Social Media'),
    ])


class SocialMediaAccount(Orderable):

    site_settings = ParentalKey(SiteSettings, on_delete=models.CASCADE, related_name='social_media_accounts')
    service = models.CharField(max_length=20, choices=get_social_media_service_choices())
    url = models.URLField()

    @property
    def icon(self) -> str:
        services = get_social_media_services()
        if self.service in services:
            return services[self.service].icon
        return ''

    @property
    def service_name(self) -> str:
        services = get_social_media_services()
        if self.service in services:
            return services[self.service].name
        return ''
