import json
from typing import Any

import requests
from django.conf import settings

from .exceptions import NetboxRequestError


def netbox_query(query: str, variables: dict[str, str] | None = None) -> dict[str, Any]:  # noqa: FA102
    payload = {
        "query": query,
    }

    if variables is not None:
        payload["variables"] = variables

    try:
        resp = requests.post(
            settings.NETBOX_GRAPHQL_ENDPOINT,
            headers={
                "Authorization": f"Token {settings.NETBOX_API_TOKEN}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=settings.NETBOX_REQUEST_TIMEOUT,
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
        except json.JSONDecodeError:
            message = str(e)
        else:
            errors = data.get("errors")
            message = f"{e}: GraphQL errors: {errors}"
        raise NetboxRequestError(message) from e

    try:
        gql_response = resp.json()
    except json.JSONDecodeError as e:
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
