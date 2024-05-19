import httpx
import pytest
from httpx import AsyncClient
from typing import Dict
from pydantic import BaseModel
from unittest.mock import patch, Mock
from daprgen.domain.ghl_oauth_schema import *
from daprgen.domain.ghl_oauth_service import GHLOAuthService
from daprgen.mixins.ghl_service_mixin import GHLServiceMixin



# Mock classes
class MockGHLServiceMixin(GHLServiceMixin):
    def __init__(self, base_url: str, auth_token: str, transport: httpx.AsyncBaseTransport):
        self.base_url = base_url
        self.auth_token = auth_token
        self.transport = transport

    async def request(self, method: str, endpoint: str, **kwargs):
        return Mock()

    def map_response(self, response, response_map):
        status_code = response.status_code
        return response_map.get(status_code, Dict[str, str])(**response.json())


@pytest.fixture
def oauth_service():
    return GHLOAuthService(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="https://example.com/oauth/callback",
        base_url="https://services.leadconnectorhq.com",
        auth_token="test_auth_token",
        transport=AsyncClient()
    )


@pytest.mark.asyncio
async def test_get_access_token(oauth_service: GHLOAuthService):
    params = GetAccessTokenPostParams(
        client_id="test_client_id",
        client_secret="test_client_secret",
        grant_type="authorization_code",
        code="test_code",
        redirect_uri="https://example.com/oauth/callback"
    )

    expected_response = {
        "access_token": "ab12dc0ae1234a7898f9ff06d4f69gh",
        "token_type": "Bearer",
        "expires_in": 86399,
        "refresh_token": "xy34dc0ae1234a4858f9ff06d4f66ba",
        "scope": "conversations/message.readonly conversations/message.write",
        "userType": "Location",
        "locationId": "l1C08ntBrFjLS0elLIYU",
        "companyId": "l1C08ntBrFjLS0elLIYU",
        "approvedLocations": ["l1C08ntBrFjLS0elLIYU"],
        "userId": "l1C08ntBrFjLS0elLIYU",
        "planId": "l1C08ntBrFjLS0elLIYU"
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json = Mock(return_value=expected_response)

    with patch.object(oauth_service, 'request', return_value=mock_response):
        response = await oauth_service.get_access_token(params)

    assert isinstance(response, GetAccessCodeSuccessfulResponseDTO)
    assert response.access_token == expected_response["access_token"]
    assert response.token_type == expected_response["token_type"]
    assert response.expires_in == expected_response["expires_in"]
    assert response.refresh_token == expected_response["refresh_token"]
    assert response.scope == expected_response["scope"]
    assert response.userType == expected_response["userType"]
    assert response.locationId == expected_response["locationId"]
    assert response.companyId == expected_response["companyId"]
    assert response.approvedLocations == expected_response["approvedLocations"]
    assert response.userId == expected_response["userId"]
    assert response.planId == expected_response["planId"]


@pytest.mark.asyncio
async def test_get_location_access_token(oauth_service: GHLOAuthService):
    params = GetLocationAccessTokenPostParams(
        companyId="test_company_id",
        locationId="test_location_id",
        version="2021-07-28"
    )

    expected_response = {
        "access_token": "ab12dc0ae1234a7898f9ff06d4f69gh",
        "token_type": "Bearer",
        "expires_in": 86399,
        "scope": "conversations/message.readonly conversations/message.write",
        "locationId": "l1C08ntBrFjLS0elLIYU",
        "userId": "l1C08ntBrFjLS0elLIYU"
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json = Mock(return_value=expected_response)

    with patch.object(oauth_service, 'request', return_value=mock_response):
        response = await oauth_service.get_location_access_token(params)

    assert isinstance(response, GetLocationAccessTokenSuccessfulResponseDTO)
    assert response.access_token == expected_response["access_token"]
    assert response.token_type == expected_response["token_type"]
    assert response.expires_in == expected_response["expires_in"]
    assert response.scope == expected_response["scope"]
    assert response.locationId == expected_response["locationId"]
    assert response.userId == expected_response["userId"]


@pytest.mark.asyncio
async def test_get_installed_location(oauth_service: GHLOAuthService):
    params = GetInstalledLocationsGetParams(
        appId="test_app_id",
        companyId="test_company_id",
        limit=10,
        query="test_query",
        skip=1
    )

    expected_response = {
        "locations": [
            {
                "_id": "0IHuJvc2ofPAAA8GzTRi",
                "name": "John Deo",
                "address": "47 W 13th St, New York, NY 10011, USA",
                "isInstalled": True
            }
        ],
        "count": 1231,
        "installToFutureLocations": True
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json = Mock(return_value=expected_response)

    with patch.object(oauth_service, 'request', return_value=mock_response):
        response = await oauth_service.get_installed_location(params)

    assert isinstance(response, GetInstalledLocationsSuccessfulResponseDTO)
    assert len(response.locations) == 1
    assert response.locations[0].id == expected_response["locations"][0]["_id"]
    assert response.locations[0].name == expected_response["locations"][0]["name"]
    assert response.locations[0].address == expected_response["locations"][0]["address"]
    assert response.locations[0].is_installed == expected_response["locations"][0]["isInstalled"]
    assert response.count == expected_response["count"]
    assert response.install_to_future_locations == expected_response["installToFutureLocations"]
