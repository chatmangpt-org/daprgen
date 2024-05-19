
from typing import Any, Dict, Type
import httpx
from pydantic import BaseModel

class GHLOAuthService:
    def __init__(self, base_url: str, auth_token: str, version: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.version = version

    async def request(self, method: str, endpoint: str, data: Any = None, params: Dict[str, Any] = None) -> Any:
        async with httpx.AsyncClient() as client:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Version': self.version,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            url = f"{self.base_url}{endpoint}"
            response = await client.request(method, url, json=data, params=params, headers=headers)
            response.raise_for_status()
            return response.json()

    def map_response(self, response: httpx.Response, response_map: Dict[int, Type[BaseModel]]) -> Any:
        response_type = response_map.get(response.status_code)
        if response_type:
            return response_type.parse_obj(response.json())
        response.raise_for_status()

    async def get_access_token(self, params: Dict[str, Any] = None) -> Any:
        response = await self.request('post', '/oauth/token', params)
        response_map = {
            200: GetAccessCodeSuccessfulResponseDto,
            400: BadRequestDTO,
            401: UnauthorizedDTO,
            422: UnprocessableDTO,
        }
        return self.map_response(response, response_map)

    async def get_location_access_token(self, params: Dict[str, Any] = None) -> Any:
        response = await self.request('post', '/oauth/locationToken', params)
        response_map = {
            200: GetLocationAccessTokenSuccessfulResponseDto,
            400: BadRequestDTO,
            401: UnauthorizedDTO,
            422: UnprocessableDTO,
        }
        return self.map_response(response, response_map)

    async def get_installed_location(self, params: Dict[str, Any] = None) -> Any:
        response = await self.request('get', '/oauth/installedLocations', params)
        response_map = {
            200: GetInstalledLocationsSuccessfulResponseDto,
            400: BadRequestDTO,
            401: UnauthorizedDTO,
            422: UnprocessableDTO,
        }
        return self.map_response(response, response_map)

