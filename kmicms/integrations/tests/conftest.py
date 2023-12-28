from collections.abc import Iterator

import pytest
import responses


@pytest.fixture
def mocked_responses() -> Iterator[responses.RequestsMock]:
    with responses.RequestsMock() as requests_mock:
        yield requests_mock
