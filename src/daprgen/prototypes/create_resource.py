import json
from typing import Dict, Any
import httpx
from pydantic import BaseModel

from daprgen.prototypes.calendar.ghl_calendar_models import CreateCalendarResourceDTO


# Assuming the necessary DTO classes are imported from ghl_calendar_models

class GHLCalendarService:
    def __init__(self, base_url: str, auth_token: str, version: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.version = version

    async def request(self, method: str, endpoint: str, data: BaseModel = None):
        async with httpx.AsyncClient() as client:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Version': self.version,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            url = f"{self.base_url}{endpoint}"
            print(f"Sending {method} request to {url} with data: {data.model_dump()}")

            json_data = data.model_dump() if data else None  # Ensure data is properly converted to dict

            response = await client.request(method, url, json=json_data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            if response.content:
                return response.json()

    async def create_calendar_resource(self, data: CreateCalendarResourceDTO, resource_type: str):
        endpoint = f'/calendars/resources/{resource_type}'
        return await self.request('post', endpoint, data)

# Import the asyncio module
import asyncio

async def main():
    # Initialize the service with test parameters
    base_url = "https://stoplight.io/mocks/highlevel/integrations/39582850"
    auth_token = "123"  # Replace with your actual token
    version = "2021-04-15"
    service = GHLCalendarService(base_url, auth_token, version)

    # Prepare the data for creating a calendar resource
    data = CreateCalendarResourceDTO(
        locationId="string",
        name="Test Equipment",
        description="Description of test equipment",
        quantity=5,
        outOfService=0,
        capacity=10,
        calendarIds=["calendarId1", "calendarId2"],
        isActive=True
    )

    try:
        # Call the create_calendar_resource method
        response = await service.create_calendar_resource(data=data, resource_type="equipments")

        # Print the response
        print(response)
    except httpx.HTTPStatusError as e:
        # Handle and print any HTTP errors
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        # Handle and print any other errors
        print(f"An error occurred: {str(e)}")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
