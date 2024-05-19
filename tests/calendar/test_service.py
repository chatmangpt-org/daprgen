import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, MockTransport, Request, Response
from daprgen.api import app  # Ensure you import your FastAPI app
from daprgen.domain.oauth_service import OAuthService
from daprgen.routes.oauth_routes import get_oauth_service
from daprgen.utils.httpx_tools import fetch_and_parse_model

def mock_exchange_code_for_token(request: Request) -> Response:
    return Response(200, json={"access_token": "fake-token", "token_type": "Bearer"})

@pytest.fixture(scope="function")
def client():
    transport = ASGITransport(app=app)
    mock_transport = MockTransport(mock_exchange_code_for_token)
    oauth_service = OAuthService("client_id", "client_secret", "redirect_uri", transport=mock_transport)

    app.dependency_overrides[get_oauth_service] = lambda: oauth_service

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
