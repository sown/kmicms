from core.blocks import StoryBlock
from django.db import models
from wagtail.admin.panels import FieldPanel, TitleFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index


class StandardPage(Page):
    content = StreamField(StoryBlock())
    show_breadcrumbs = models.BooleanField(help_text="Show breadcrumbs at top of page?", default=True)
    show_title = models.BooleanField(help_text="Show page title at top of page?", default=True)

    parent_page_types = ["home.HomePage", "standard_page.StandardPage"]
    subpage_types = ["standard_page.StandardPage", "contact.ContactFormPage", "infra.NetboxInfrastructurePage"]

    content_panels = [
        TitleFieldPanel("title"),
        FieldPanel("content"),
    ]

    settings_panels = [
        FieldPanel("show_title"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("content"),
    ]
