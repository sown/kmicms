from __future__ import annotations

from http import HTTPStatus
from typing import Any

import pytest
from responses import RequestsMock, matchers

from integrations.netbox import NetboxClient


class TestNetboxClient:
    @pytest.fixture
    def client(self) -> NetboxClient:
        return NetboxClient(
            graphql_endpoint="https://netbox.invalid/graphql/",
            api_token="abc",  # noqa: S106
            cache_ttl_seconds=300,
            request_timeout=0.5,
        )

    def test_get_headers(self, client: NetboxClient) -> None:
        expected_headers = {
            "Authorization": "Token abc",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        assert expected_headers == client._get_headers()

    @pytest.mark.parametrize(
        ("query", "variables", "expected_payload"),
        [
            pytest.param("query", None, {"query": "query"}, id="no-variables"),
            pytest.param("query", {}, {"query": "query", "variables": {}}, id="empty-variables"),
            pytest.param("query", {"a": 1}, {"query": "query", "variables": {"a": 1}}, id="variables"),
        ],
    )
    def test_get_payload(
        self,
        client: NetboxClient,
        query: str,
        variables: dict[str, str] | None,
        expected_payload: dict[str, Any],
    ) -> None:
        assert client._get_payload(query, variables) == expected_payload

    def test_query(self, client: NetboxClient, mocked_responses: RequestsMock) -> None:
        mocked_responses.post(
            "https://netbox.invalid/graphql/",
            match=[
                matchers.header_matcher(
                    {"Content-Type": "application/json", "Accept": "application/json", "Authorization": "Token abc"},
                ),
            ],
            json={"data": {"a": "b"}},
            status=HTTPStatus.OK,
            content_type="application/json",
        )
        data = client._query("query")
        assert data == {"a": "b"}
