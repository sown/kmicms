from typing import Any

from django.conf import settings
from django.core.cache import cache

from .graphql import netbox_query
from .queries import GET_DEVICE_QUERY, GET_VM_QUERY, LIST_DEVICE_QUERY, LIST_VM_QUERY


class NetboxClient:
    def __init__(self, *, cache_ttl_seconds: int = settings.NETBOX_CACHE_TTL) -> None:
        self.cache_ttl_seconds = cache_ttl_seconds

    def get_device(self, device_id: int) -> dict[str, Any]:
        cache_key = f"netbox__device__{device_id}"

        if cache_value := cache.get(cache_key):
            return cache_value

        device = netbox_query(GET_DEVICE_QUERY, {"deviceId": device_id})["device"]
        cache.set(cache_key, device, timeout=self.cache_ttl_seconds)

        return device

    def get_vm(self, vm_id: int) -> dict[str, Any]:
        cache_key = f"netbox__vm__{vm_id}"

        if cache_value := cache.get(cache_key):
            return cache_value

        vm = netbox_query(GET_VM_QUERY, {"VMId": vm_id})["virtual_machine"]
        cache.set(cache_key, vm, timeout=self.cache_ttl_seconds)

        return vm

    def list_devices(
        self,
    ) -> dict[str, Any]:
        cache_key = "netbox__device_list"

        if cache_value := cache.get(cache_key):
            return cache_value

        device = netbox_query(LIST_DEVICE_QUERY)["device_list"]
        cache.set(cache_key, device, timeout=self.cache_ttl_seconds)

        return device

    def list_vms(
        self,
    ) -> dict[str, Any]:
        cache_key = "netbox__vm_list"

        if cache_value := cache.get(cache_key):
            return cache_value

        vms = netbox_query(LIST_VM_QUERY)["virtual_machine_list"]
        cache.set(cache_key, vms, timeout=self.cache_ttl_seconds)

        return vms
