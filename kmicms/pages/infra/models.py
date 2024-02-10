from typing import Any

from core.blocks import StoryBlock
from django.db import models
from django.db.models.functions import Lower
from django.http import HttpRequest
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, TitleFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page


class NetboxInfrastructurePage(Page):
    max_count = 1
    # Intentionally empty to prevent manual creation of device and VM pages
    subpage_types = []

    content = StreamField(StoryBlock())

    content_panels = [
        TitleFieldPanel("title"),
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Netbox Index Page"

    def get_entity_pages(self, request: HttpRequest) -> models.QuerySet["NetboxEntityPage"]:
        return NetboxEntityPage.objects.child_of(self).live().order_by(Lower("title"))

    def get_context(self, request: HttpRequest, *args: Any, **kwargs: Any) -> dict[Any]:
        ctx = super().get_context(request, *args, **kwargs)
        ctx["entity_results"] = self.get_entity_pages(request)
        return ctx


class NetboxEntityType(models.TextChoices):
    DEVICE = "DEV", "Physical Device"
    VM = "VM", "Virtual Machine"


class NetboxEntityPage(Page):
    parent_page_types = ["infra.NetboxInfrastructurePage"]
    subpage_types = []

    netbox_name = models.CharField(max_length=255)
    netbox_id = models.IntegerField(verbose_name="Netbox ID")
    netbox_entity_type = models.CharField(max_length=3, choices=NetboxEntityType.choices)
    netbox_data = models.JSONField()

    content_panels = [
        TitleFieldPanel("title"),
        MultiFieldPanel(
            [
                FieldPanel("netbox_name", read_only=True),
                FieldPanel("netbox_entity_type", read_only=True),
                FieldPanel("netbox_id", read_only=True),
            ],
            heading="Netbox Info",
        ),
    ]

    class Meta:
        verbose_name = "Netbox Entity Page"
        constraints = [
            models.UniqueConstraint(fields=["netbox_id", "netbox_entity_type"], name="unique_id_for_netbox_entity")
        ]
