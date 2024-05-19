import httpx
from pydantic import BaseModel
from typing import Type, TypeVar

Model = TypeVar('Model', bound=BaseModel)


async def fetch_and_parse_model(
    url: str,
    headers: dict,
    data: dict,
    model_class: Type[Model],
    transport: httpx.AsyncBaseTransport
) -> Model:
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_data = response.json()
        return model_class(**response_data)
