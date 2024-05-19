import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pyngrok import ngrok, conf
from daprgen.routes import app, get_access_token
from dotenv import load_dotenv

from ngrok_config import create_ngrok_tunnel

# Load environment variables from .env file
load_dotenv()


# Fixture to start and stop the FastAPI app
@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client


def test_ngrok_tunnel_creation(mock_ngrok_tunnel):
    domain = "chatmangpt.ngrok.dev"
    port = 8000
    tunnel = create_ngrok_tunnel(domain, port)
    assert tunnel == "https://chatmangpt.ngrok.dev"


@pytest.mark.asyncio
async def test_oauth_callback_success(mock_ngrok_tunnel, monkeypatch):
    async def mock_get_access_token(code: str):
        return {"access_token": "mocked_access_token"}

    monkeypatch.setattr("daprgen.api.get_access_token", mock_get_access_token)

    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/oauth/callback/gohighlevel?code=mocked_code")
        assert response.status_code == 200
        assert response.json() == {"access_token": "mocked_access_token"}


@pytest.mark.asyncio
async def test_oauth_callback_no_code(mock_ngrok_tunnel):
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/oauth/callback/gohighlevel")
        assert response.status_code == 200
        assert response.json() == {"error": "Authorization code not found"}


@pytest.mark.asyncio
async def test_get_access_token_success(mock_ngrok_tunnel, monkeypatch):
    class MockResponse:
        status_code = 200

        def json(self):
            return {"access_token": "mocked_access_token"}

        @property
        def text(self):
            return '{"access_token": "mocked_access_token"}'

        def raise_for_status(self):
            pass

    async def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    app.state.public_url = "https://chatmangpt.ngrok.dev"  # Ensure the public_url is set during the test

    response = await get_access_token("mocked_code")
    assert response["access_token"] == "mocked_access_token"
