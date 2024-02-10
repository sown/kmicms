from django.conf import settings
from django.core.management.base import BaseCommand
from integrations.netbox.client import NetboxClient

from pages.infra.models import NetboxEntityPage, NetboxEntityType, NetboxInfrastructurePage


class Command(BaseCommand):
    help = "Synchronise pages that are created from Netbox"  # noqa: A003

    def handle(
        self,
        *,
        verbosity: int,
        settings: str,
        pythonpath: str,
        traceback: bool,
        no_color: bool,
        force_color: bool,
        skip_checks: bool,
    ) -> None:
        # We only expect there to be one index, but to be sure...
        assert NetboxInfrastructurePage.objects.count() == 1
        index_page = NetboxInfrastructurePage.objects.first()
        client = self._get_client()
        self._sync_pages(index_page, client.list_devices(), NetboxEntityType.DEVICE)
        self._sync_pages(index_page, client.list_vms(), NetboxEntityType.VM)
        self.stdout.write("Synchronised all netbox pages")

    def _sync_pages(self, parent: NetboxInfrastructurePage, entities: list, entity_type: NetboxEntityType) -> None:
        synced_entity_page_ids: list[int] = []

        entity_pages_qs = NetboxEntityPage.objects.child_of(parent).filter(
            netbox_entity_type=entity_type,
        )

        for entity in entities:
            try:
                entity_page = entity_pages_qs.get(
                    netbox_id=entity["id"],
                )
                if entity_page.netbox_name != entity["name"]:
                    entity_page.netbox_name = entity["name"]

                if entity_page.netbox_data != entity:
                    entity_page.netbox_data = entity

                # TODO: Only save if needed, check update
                entity_page.save()
            except NetboxEntityPage.DoesNotExist:
                entity_page = NetboxEntityPage(
                    title=entity["name"],
                    netbox_id=entity["id"],
                    netbox_name=entity["name"],
                    netbox_entity_type=entity_type,
                    netbox_data=entity,
                )
                parent.add_child(instance=entity_page)

            synced_entity_page_ids.append(entity_page.id)

        # Unpublish any entities that no longer exist in Netbox
        entities_to_unpublish = entity_pages_qs.exclude(id__in=synced_entity_page_ids).live()
        for entity_page in entities_to_unpublish:
            self.stdout.write(f"Unpublishing {entity_page} as it was deleted in Netbox")
            entity_page.unpublish()

    def _get_client(self) -> NetboxClient:
        return NetboxClient(
            graphql_endpoint=settings.NETBOX_GRAPHQL_ENDPOINT,
            api_token=settings.NETBOX_API_TOKEN,
            cache_ttl_seconds=settings.NETBOX_CACHE_TTL,
            request_timeout=settings.NETBOX_REQUEST_TIMEOUT,
        )
