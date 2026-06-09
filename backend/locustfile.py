"""Locust load test for ESBot session API (no LLM-dependent endpoints).

Run:
    ./performance/scripts/start-api-for-perf.sh   # in another terminal
    uv run locust -f locustfile.py --host http://localhost:8000

For JMeter and Gatling, see performance/README.md.

Requires: uv pip install locust
"""

from locust import HttpUser, between, task


class ESBotUser(HttpUser):
    """Simulated user exercising session and health endpoints only."""

    wait_time = between(1, 3)

    def on_start(self) -> None:
        """Create a session before running tasks."""
        response = self.client.post(
            "/api/v1/sessions",
            json={"user_id": "load-test-user", "title": "Load Test"},
        )
        response.raise_for_status()
        self.session_id = response.json()["id"]

    @task(3)
    def get_session(self) -> None:
        """Read session metadata."""
        self.client.get(f"/api/v1/sessions/{self.session_id}")

    @task(2)
    def list_sessions(self) -> None:
        """List sessions for the test user."""
        self.client.get("/api/v1/sessions", params={"user_id": "load-test-user"})

    @task(2)
    def get_message_history(self) -> None:
        """Read message history (empty unless populated elsewhere)."""
        self.client.get(f"/api/v1/sessions/{self.session_id}/messages")

    @task(1)
    def health_check(self) -> None:
        """Hit health endpoint."""
        self.client.get("/api/v1/health")
