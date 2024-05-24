from httpx import AsyncClient
import os
import json
import base64
from Crypto.Cipher import AES
from loguru import logger
from daprgen.model import Model, InstallationDetails, AppUserType, TokenType

GHL_API_DOMAIN = os.getenv("GHL_API_DOMAIN")
GHL_CLIENT_ID = os.getenv("GHL_APP_CLIENT_ID")
GHL_CLIENT_SECRET = os.getenv("GHL_APP_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

class GHL:
    def __init__(self, model: Model, client: AsyncClient):
        self.model = model
        self.client = client

    async def authorization_handler(self, code):
        if not code:
            logger.warning("Please provide code when making call to authorization Handler")
        await self.generate_access_token_refresh_token_pair(code)

    async def decrypt_sso_data(self, key):
        secret = os.getenv("GHL_APP_SSO_KEY")
        cipher = AES.new(secret.encode('utf-8'), AES.MODE_EAX, nonce=key[:16].encode('utf-8'))
        data = cipher.decrypt(base64.b64decode(key[16:])).decode('utf-8')
        return json.loads(data)

    async def refresh_access_token(self, resource_id):
        try:
            resp = await self.client.post(
                f"{GHL_API_DOMAIN}/oauth/token",
                data={
                    'client_id': GHL_CLIENT_ID,
                    'client_secret': GHL_CLIENT_SECRET,
                    'grant_type': 'refresh_token',
                    'refresh_token': self.model.get_refresh_token(resource_id),
                },
                headers={'content-type': 'application/x-www-form-urlencoded'}
            )
            resp_data = resp.json()
            self.model.set_access_token(resource_id, resp_data['access_token'])
            self.model.set_refresh_token(resource_id, resp_data['refresh_token'])
        except Exception as e:
            logger.error(f"Error refreshing access token: {e}")

    async def generate_access_token_refresh_token_pair(self, code):
        try:
            resp = await self.client.post(
                f"{GHL_API_DOMAIN}/oauth/token",
                data={
                    'client_id': GHL_CLIENT_ID,
                    'client_secret': GHL_CLIENT_SECRET,
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': REDIRECT_URI,
                },
                headers={'content-type': 'application/x-www-form-urlencoded'}
            )
            resp_data = resp.json()
            logger.debug(f"Token pair generated: {resp_data}")
            details = InstallationDetails.model_validate(resp_data)  # Adjust userType as necessary
            self.model.save_installation_info(details)
        except Exception as e:
            logger.error(f"Error generating token pair: {e}")

    async def requests(self, resource_id):
        if not self.model.get_access_token(resource_id):
            raise Exception("Installation not found for the following resource")

        async def request_interceptor(request):
            request.headers['Authorization'] = f"Bearer {self.model.get_access_token(resource_id)}"
            return request

        async def response_interceptor(response):
            if response.status_code == 401:
                original_request = response.request
                if not getattr(original_request, '_retry', False):
                    original_request._retry = True
                    await self.refresh_access_token(resource_id)
                    original_request.headers['Authorization'] = f"Bearer {self.model.get_access_token(resource_id)}"
                    return await self.client.send(original_request)
            return response

        self.client.event_hooks = {
            'request': [request_interceptor],
            'response': [response_interceptor],
        }
        return self.client
