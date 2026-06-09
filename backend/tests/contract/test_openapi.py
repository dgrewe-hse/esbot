"""Contract tests against the OpenAPI schema (optional, skipped in default CI)."""

import pytest

pytestmark = [
    pytest.mark.contract,
    pytest.mark.skip(reason="Contract tests enabled in a later lab"),
]


def test_openapi_schema_available(client):
    """Verify OpenAPI schema is exposed."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "ESBot API"
    assert "/api/v1/sessions" in schema["paths"]
