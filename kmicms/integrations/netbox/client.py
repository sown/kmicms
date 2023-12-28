from __future__ import annotations

from typing import Any

import requests
from django.core.cache import cache

from .exceptions import NetboxRequestError
from .queries import GET_DEVICE_QUERY, GET_VM_QUERY, LIST_DEVICE_QUERY, LIST_VM_QUERY


class NetboxClient:
    def __init__(
        self, *, graphql_endpoint: str, api_token: str, cache_ttl_seconds: int, request_timeout: float
    ) -> None:
        self.graphql_endpoint = graphql_endpoint
        self.api_token = api_token
        self.cache_ttl_seconds = cache_ttl_seconds
        self.request_timeout = request_timeout

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Token {self.api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _get_payload(self, query: str, variables: dict[str, str] | None = None) -> dict[str, str]:
        payload = {
            "query": query,
        }

        if variables is not None:
            payload["variables"] = variables

        return payload

    def _query(self, query: str, variables: dict[str, str] | None = None) -> dict[str, Any]:  # noqa: FA102
        payload = self._get_payload(query, variables)

        try:
            resp = requests.post(
                self.graphql_endpoint,
                headers=self._get_headers(),
                json=payload,
                timeout=self.request_timeout,
            )
        except ConnectionError as e:
            raise NetboxRequestError("Unable to connect to netbox") from e
        except requests.RequestException as e:
            raise NetboxRequestError("Error when requesting data from netbox") from e

        try:
            resp.raise_for_status()
        except requests.RequestException as e:
            # Include GraphQL errors in the exception message.
            try:
                data = resp.json()
            except requests.exceptions.JSONDecodeError:
                message = str(e)
            else:
                errors = data.get("errors")
                message = f"{e}: GraphQL errors: {errors}"
            raise NetboxRequestError(message) from e

        try:
            gql_response = resp.json()
        except requests.exceptions.JSONDecodeError as e:
            raise NetboxRequestError("Netbox returned invalid JSON") from e

        # Check for and raise any GraphQL errors from successful responses.
        if "errors" in gql_response:
            errors = gql_response["errors"]
            raise NetboxRequestError(f"Invalid GraphQL response: {errors}")

        try:
            return gql_response["data"]
        except KeyError as e:
            raise NetboxRequestError(
                "Netbox API response did not contain data.",
            ) from e

    def get_device(self, device_id: int) -> dict[str, Any]:
        cache_key = f"netbox__device__{device_id}"

        if cache_value := cache.get(cache_key):
            return cache_value

        device = self._query(GET_DEVICE_QUERY, {"deviceId": device_id})["device"]
        cache.set(cache_key, device, timeout=self.cache_ttl_seconds)

        return device

    def get_vm(self, vm_id: int) -> dict[str, Any]:
        cache_key = f"netbox__vm__{vm_id}"

        if cache_value := cache.get(cache_key):
            return cache_value

        vm = self._query(GET_VM_QUERY, {"VMId": vm_id})["virtual_machine"]
        cache.set(cache_key, vm, timeout=self.cache_ttl_seconds)

        return vm

    def list_devices(
        self,
    ) -> dict[str, Any]:
        cache_key = "netbox__device_list"

        if cache_value := cache.get(cache_key):
            return cache_value

        device = self._query(LIST_DEVICE_QUERY)["device_list"]
        cache.set(cache_key, device, timeout=self.cache_ttl_seconds)

        return device

    def list_vms(
        self,
    ) -> dict[str, Any]:
        cache_key = "netbox__vm_list"

        if cache_value := cache.get(cache_key):
            return cache_value

        vms = self._query(LIST_VM_QUERY)["virtual_machine_list"]
        cache.set(cache_key, vms, timeout=self.cache_ttl_seconds)

        return vms
