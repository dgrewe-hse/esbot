from sqlalchemy import inspect, text

from app.config import settings
from app.database import Base
from tests.conftest import test_engine


class TestAppImport:
    def test_app_is_importable(self):
        from app.main import app
        assert app is not None

    def test_app_has_correct_title(self):
        from app.main import app
        assert app.title == "ESBot Backend API"


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self, client):
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "esbot-backend"

    def test_health_response_is_json(self, client):
        response = client.get("/health")
        assert isinstance(response.json(), dict)


class TestDatabaseSetup:
    def test_base_has_metadata(self):
        assert Base is not None
        assert hasattr(Base, "metadata")

    def test_test_engine_connects(self):
        with test_engine.connect() as conn:
            row = conn.execute(text("SELECT 1")).fetchone()
        assert row[0] == 1

    def test_create_all_runs_without_error(self):
        # create_all soll auch ohne definierte Entities nicht crashen
        Base.metadata.create_all(bind=test_engine)
        tables = inspect(test_engine).get_table_names()
        assert isinstance(tables, list)
        Base.metadata.drop_all(bind=test_engine)


class TestConfiguration:
    def test_database_url_is_set(self):
        assert settings.database_url

    def test_app_env_is_valid(self):
        assert settings.app_env in ("development", "test", "production")
