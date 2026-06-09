"""Locust load test stub for ESBot API (Exercise: Performance Testing).

Run manually when ready:
    uv run locust -f locustfile.py --host http://localhost:8000

Requires: pip install locust (not included in default dev dependencies).
"""

from locust import HttpUser, between, task


class ESBotUser(HttpUser):
    """Simulated user interacting with ESBot REST API."""

    wait_time = between(1, 3)

    def on_start(self) -> None:
        """Create a session before running tasks."""
        response = self.client.post(
            "/api/v1/sessions",
            json={"user_id": "load-test-user", "title": "Load Test"},
        )
        self.session_id = response.json()["id"]

    @task(3)
    def send_message(self) -> None:
        """Send a chat message."""
        self.client.post(
            f"/api/v1/sessions/{self.session_id}/messages",
            json={"content": "What is unit testing?"},
        )

    @task(1)
    def health_check(self) -> None:
        """Hit health endpoint."""
        self.client.get("/api/v1/health")
