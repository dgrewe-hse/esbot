"""Performance smoke tests (optional, skipped in default CI)."""

import pytest

pytestmark = [
    pytest.mark.performance,
    pytest.mark.skip(reason="Performance tests enabled in a later lab"),
]


def test_health_endpoint_benchmark(benchmark, client):
    """Benchmark health endpoint response time."""
    benchmark(lambda: client.get("/api/v1/health"))
