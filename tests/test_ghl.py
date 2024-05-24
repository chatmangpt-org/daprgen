import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from daprgen.api import app
from daprgen.ghl import GHL, Model
from pytest_httpx import HTTPXMock

from daprgen.model import InstallationDetails


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def model():
    return Model()


@pytest.fixture
def ghl(model):
    return GHL(model, AsyncClient())


@pytest.fixture
def token(model):
    details = InstallationDetails.model_validate({
        "access_token": "mock_access_token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_token": "mock_refresh_token",
        "scope": "conversations.message.readonly conversations.message.write",
        "userType": "Company",
        "companyId": "mock_company_id",
        "locationId": "mock_location_id"
    })
    return details


@pytest.mark.asyncio
async def test_authorize(httpx_mock: HTTPXMock):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/authorize",
                                    params={"scopes": "conversations.message.readonly conversations.message.write"})
    assert response.status_code == 307
    assert "location" in response.headers


@pytest.mark.asyncio
async def test_oauth_callback(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://services.leadconnectorhq.com/oauth/token",
        json={
            "access_token": "mock_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "mock_refresh_token",
            "scope": "conversations.message.readonly conversations.message.write"
        }
    )
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/oauth/callback", params={"code": "mock_code"})
    assert response.status_code == 307
    assert response.headers["location"] == "https://app.gohighlevel.com/"


@pytest.mark.asyncio
async def test_example_api_call(httpx_mock: HTTPXMock, model: Model, token: InstallationDetails):
    httpx_mock.add_response(
        url=f"https://services.leadconnectorhq.com/users/search?companyId={token.company_id}",
        json={"users": [{"id": "123", "name": "Test User"}]}
    )
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/example-api-call", params={"companyId": token.company_id})
    assert response.status_code == 200
    assert response.json() == {"users": [{"id": "123", "name": "Test User"}]}


@pytest.mark.asyncio
async def test_example_api_call_location(httpx_mock: HTTPXMock, model: Model, token: InstallationDetails):
    httpx_mock.add_response(
        url="https://services.leadconnectorhq.com/contacts/?locationId=mock_location_id",
        json={"contacts": [{"id": "456", "name": "Test Contact"}]}
    )
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/example-api-call-location", params={"companyId": token.company_id,
                                                                              "locationId": token.location_id})
    assert response.status_code == 200
    assert response.json() == {"contacts": [{"id": "456", "name": "Test Contact"}]}


@pytest.mark.asyncio
async def test_example_webhook_handler():
    payload = {"event": "test_event", "data": {"key": "value"}}
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/example-webhook-handler", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "received"}


@pytest.mark.asyncio
async def test_decrypt_sso(httpx_mock: HTTPXMock, mocker):
    mocker.patch("daprgen.ghl.GHL.decrypt_sso_data", return_value={"user": "test_user"})
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/decrypt-sso", json={"key": "mock_key"})
    assert response.status_code == 200
    assert response.json() == {"user": "test_user"}
