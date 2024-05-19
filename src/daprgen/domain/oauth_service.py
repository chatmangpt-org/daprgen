import httpx
from daprgen.domain.oauth_models import OAuthToken

from daprgen.utils.httpx_tools import fetch_and_parse_model


class OAuthService:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, transport: httpx.AsyncBaseTransport):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.transport = transport

    def get_authorization_url(self) -> str:
        # Business logic to generate authorization URL
        return "https://example.com/oauth/authorize"

    async def exchange_code_for_token(self, code: str) -> OAuthToken:
        url = 'https://services.leadconnectorhq.com/oauth/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
        }
        return await fetch_and_parse_model(url, headers, data, OAuthToken, self.transport)
