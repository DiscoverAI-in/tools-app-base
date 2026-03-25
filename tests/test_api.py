import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.anyio
async def test_health(client):
    r = await client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"


@pytest.mark.anyio
async def test_home_page(client):
    r = await client.get("/")
    assert r.status_code == 200
    assert "FastAPI Apps" in r.text


@pytest.mark.anyio
async def test_app_page(client):
    r = await client.get("/source-to-final")
    assert r.status_code == 200
    assert "Source to Final" in r.text


@pytest.mark.anyio
async def test_404_app(client):
    r = await client.get("/nonexistent-app")
    assert r.status_code == 404
