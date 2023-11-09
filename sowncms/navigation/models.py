from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField

from .blocks import FooterMenuBlock, MainMenuBlock


@register_setting(icon="list-ul")
class NavigationSettings(BaseSiteSetting, ClusterableModel):

    main_menu = StreamField(MainMenuBlock(), use_json_field=True)
    footer_menu = StreamField(FooterMenuBlock(), use_json_field=True)


    panels = [
        FieldPanel("main_menu"),
        FieldPanel("footer_menu"),
    ]
