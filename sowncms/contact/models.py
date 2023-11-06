from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel, MultiFieldPanel, InlinePanel
)
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import FormMixin, AbstractFormField

from integrations.discord import submit_discord_webhook_for_form

class FormField(AbstractFormField):
    page = ParentalKey('ContactFormPage', on_delete=models.CASCADE, related_name='form_fields')


class AbstractDiscordFormPage(FormMixin, Page):

    discord_message_content = models.TextField(
        default="A form has been submitted.",
        help_text="A message that should appear before the form submission data",
        max_length=2000,
    )
    discord_webhook = models.URLField(help_text="The Discord webhook that a payload should be sent to")

    class Meta:
        abstract = True

    settings_panels = [
        MultiFieldPanel([
            FieldPanel("discord_message_content"),
            FieldPanel("discord_webhook"),
        ], heading="Discord Settings")
    ]

    def process_form_submission(self, form):
        submission = super().process_form_submission(form)
        submit_discord_webhook_for_form(
            self.discord_webhook,
            self.discord_message_content,
            submission,
        )
        return submission

class ContactFormPage(AbstractDiscordFormPage):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    parent_page_types = ["home.HomePage", "standard_page.StandardPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
    ]
