from wagtail.admin.panels import FieldPanel, TitleFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from core.blocks import BodyBlock


class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["standard_page.StandardPage", "contact.ContactFormPage", "infra.NetboxInfrastructurePage"]

    content = StreamField(BodyBlock(), use_json_field=True)

    content_panels = [
        TitleFieldPanel("title"),
        FieldPanel("content"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("content"),
    ]
