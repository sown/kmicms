from core.blocks import StoryBlock
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from integrations.netbox import NetboxClient, NetboxRequestError
from wagtail.admin.panels import FieldPanel, TitleFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class NetboxInfrastructurePage(RoutablePageMixin, Page):
    max_count = 1
    subpage_types = []

    content = StreamField(StoryBlock(), use_json_field=True)
    device_description = RichTextField()
    vm_description = RichTextField()

    content_panels = [
        TitleFieldPanel("title"),
        FieldPanel("content"),
        FieldPanel("device_description"),
        FieldPanel("vm_description"),
    ]

    def _get_client(self) -> NetboxClient:
        return NetboxClient(
            graphql_endpoint=settings.NETBOX_GRAPHQL_ENDPOINT,
            api_token=settings.NETBOX_API_TOKEN,
            cache_ttl_seconds=settings.NETBOX_CACHE_TTL,
            request_timeout=settings.NETBOX_REQUEST_TIMEOUT,
        )

    def _handle_error(self, request: HttpRequest) -> HttpResponse:
        return self.render(
            request,
            template="infra/netbox_error.html",
        )

    @path("devices/", name="device_index")
    def device_index(self, request: HttpRequest) -> HttpResponse:
        try:
            client = self._get_client()
            devices = client.list_devices()
        except NetboxRequestError:
            return self._handle_error(request)

        return self.render(
            request,
            context_overrides={"devices": devices},
            template="infra/netbox_device_index.html",
        )

    @path("devices/<int:device_id>/", name="device_view")
    def device_info(self, request: HttpRequest, *, device_id: int) -> HttpResponse:
        try:
            client = self._get_client()
            device = client.get_device(device_id)
        except NetboxRequestError:
            return self._handle_error(request)

        if device is None:
            raise Http404()

        return self.render(request, context_overrides={"device": device}, template="infra/netbox_device_view.html")

    @path("vm/", name="vm_index")
    def vm_index(self, request: HttpRequest) -> HttpResponse:
        try:
            client = self._get_client()
            vms = client.list_vms()
        except NetboxRequestError:
            return self._handle_error(request)
        return self.render(request, context_overrides={"vms": vms}, template="infra/netbox_vm_index.html")

    @path("vm/<int:vm_id>/", name="vm_view")
    def vm_info(self, request: HttpRequest, *, vm_id: int) -> HttpResponse:
        try:
            client = self._get_client()
            vm = client.get_vm(vm_id)
        except NetboxRequestError:
            return self._handle_error(request)

        if vm is None:
            raise Http404()

        return self.render(request, context_overrides={"vm": vm}, template="infra/netbox_vm_view.html")
