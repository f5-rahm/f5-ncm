import pytest

from next import NEXT


@pytest.fixture
def next_instantiation():
    return NEXT('cm', 'admin', 'CMletmein00!', session_verify=False)


def test_bearer_token_attributes_at_login(next_instantiation):
    assert next_instantiation.token_access is not None
    assert next_instantiation.token_refresh is not None
    assert next_instantiation.refresh_timestamp is None


def test_load_api_spec_attribute_at_login(next_instantiation):
    assert '/api/v1/spaces/default/analytics/access/metrics' in next_instantiation.valid_api_paths
