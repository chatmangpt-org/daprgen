from typing import Union, Dict

import httpx

from daprgen.domain.ghl_oauth_schema import *
from daprgen.mixins.ghl_service_mixin import GHLServiceMixin


class GHLOAuthService(GHLServiceMixin):
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, base_url: str, auth_token: str, transport: httpx.AsyncBaseTransport):
        super().__init__(base_url, auth_token, transport)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self) -> str:
        return "https://example.com/oauth/authorize"

    async def get_access_token(self, data: GetAccessTokenPostParams) -> Union[GetAccessCodeSuccessfulResponseDTO, BadRequestDTO, UnauthorizedDTO, UnprocessableDTO, Dict[str, str]]:
        endpoint = '/oauth/token'
        response = await self.request('post', endpoint, data=data)
        response_map = {
            200: GetAccessCodeSuccessfulResponseDTO,
            400: BadRequestDTO,
            401: UnauthorizedDTO,
            422: UnprocessableDTO,
        }
        return self.map_response(response, response_map)

    async def get_location_access_token(self, data: GetLocationAccessTokenPostParams) -> Union[GetLocationAccessTokenSuccessfulResponseDTO, BadRequestDTO, UnauthorizedDTO, UnprocessableDTO, Dict[str, str]]:
        endpoint = '/oauth/locationToken'
        response = await self.request('post', endpoint, data=data)
        response_map = {
            200: GetLocationAccessTokenSuccessfulResponseDTO,
            400: BadRequestDTO,
            401: UnauthorizedDTO,
            422: UnprocessableDTO,
        }
        return self.map_response(response, response_map)

    async def get_installed_location(self, params: GetInstalledLocationsGetParams) -> Union[GetInstalledLocationsSuccessfulResponseDTO, BadRequestDTO, UnauthorizedDTO, UnprocessableDTO, Dict[str, str]]:
        endpoint = '/oauth/installedLocations'
        response = await self.request('get', endpoint, params=params)
        response_map = {
            200: GetInstalledLocationsSuccessfulResponseDTO,
            400: BadRequestDTO,
            401: UnauthorizedDTO,
            422: UnprocessableDTO,
        }
        return self.map_response(response, response_map)
