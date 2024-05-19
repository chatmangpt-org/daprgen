import httpx
import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport

from daprgen.api import app
from daprgen.domain.oauth_models import OAuthToken
from daprgen.routes.oauth_routes import get_oauth_service


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client

# Define a mock OAuthService
class MockOAuthService:
    async def exchange_code_for_token(self, code: str) -> OAuthToken:
        return OAuthToken(
            access_token="mocked_access_token",
            refresh_token="mocked_refresh_token",
            expires_in=3600,
            scope="mocked_scope",
            token_type="Bearer"
        )

# Override the dependency
app.dependency_overrides[get_oauth_service] = lambda: MockOAuthService()

@pytest.mark.asyncio
async def test_oauth_callback_success(test_app):
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/oauth/callback/gohighlevel?code=mocked_code")
        assert response.status_code == 200
        assert response.json() == {
            "access_token": "mocked_access_token",
            "refresh_token": "mocked_refresh_token",
            "expires_in": 3600,
            "scope": "mocked_scope",
            "token_type": "Bearer"
        }