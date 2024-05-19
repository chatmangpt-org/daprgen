from typing import Any, Dict, Type, TypeVar, Union
import httpx
from pydantic import BaseModel
from functools import wraps

Model = TypeVar('Model', bound=BaseModel)


# Mixin for response mapping and request handling
class GHLServiceMixin:
    def __init__(self, base_url: str, auth_token: str, transport: httpx.AsyncBaseTransport):
        self.base_url = base_url
        self.auth_token = auth_token
        self.transport = transport

    async def request(self, method: str, endpoint: str, data: Model = None, params: Model = None, headers: Dict[str, str] = None) -> httpx.Response:
        if headers is None:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        async with httpx.AsyncClient(transport=self.transport) as client:
            url = f"{self.base_url}{endpoint}"
            response = await client.request(method, url, json=data.model_dump(), params=params.model_dump(), headers=headers)
            response.raise_for_status()
            return response

    async def fetch_and_parse_model(self, method: str, endpoint: str, data: Any, model_class: Type[Model]) -> Model:
        response = await self.request(method, endpoint, data=data)
        return model_class.model_validate(response.json())

    def map_response(self, response: httpx.Response, response_map: Dict[int, Type[BaseModel]]) -> Any:
        response_type = response_map.get(response.status_code)
        model = response_type.model_validate(response.json())
        response.raise_for_status()
        return model
