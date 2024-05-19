import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport

from daprgen.api import app
from daprgen.domain.oauth_service import OAuthService

@pytest.fixture(scope="function")
def client():
    transport = ASGITransport(app=app)
    oauth_service = OAuthService("client_id", "client_secret", "redirect_uri", transport=transport)

    with TestClient(app) as client:
        yield client

def test_oauth_callback(client):
    response = client.get("/oauth/callback/gohighlevel?code=testcode")
    assert response.status_code == 200
    assert response.json() == {"access_token": "fake-token", "token_type": "Bearer"}

def test_oauth_callback_no_code(client):
    response = client.get("/oauth/callback/gohighlevel")
    assert response.status_code == 200
    assert response.json() == {"error": "Authorization code not found"}
