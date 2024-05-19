import json
from typing import Dict
import httpx
import icontract

from daprgen.prototypes.calendar.ghl_calendar_models import *


class GHLCalendarService:
    def __init__(self, base_url: str, auth_token: str, version: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.version = version

    async def request(self, method: str, endpoint: str, data: BaseModel = None, params: Dict = None):
        async with httpx.AsyncClient() as client:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Version': self.version,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            url = f"{self.base_url}{endpoint}"

            json_data = data.model_dump() if data else None  # Ensure data is properly converted to dict

            response = await client.request(method, url, json=json_data, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors

            if response.content:
                return response.json()

    async def get_groups(self, location_id: str = None):
        response = await self.request('get', '/calendars/groups', params={'locationId': location_id})
        groups = [GroupDTO.model_validate(group) for group in response["groups"]]
        return groups
    
    async def create_calendar_group(self, data: GroupDTO = None):
        return await self.request('post', '/calendars/groups', data)
    
    async def validate_groups_slug(self, data: ValidateGroupSlugPostBody = None):
        return await self.request('post', '/calendars/groups/validate-slug', data)
    
    async def delete_group(self, group_id: str = None):
        return await self.request('delete', f'/calendars/groups/{group_id}')
    
    async def edit_group(self, data: GroupUpdateDTO = None, group_id: str = None):
        return await self.request('put', f'/calendars/groups/{group_id}', data)
    
    async def disable_group(self, data: GroupStatusUpdateParams = None, group_id: str = None):
        return await self.request('put', f'/calendars/groups/{group_id}/status', data)
    
    async def get_calendar_events(self, start_time: str, end_time: str, location_id: str, calendar_id: str) -> List[CalendarEventDTO]:
        result = await self.request('get',
                                  endpoint='/calendars/events',
                                  params={
                                      'startTime': start_time,
                                      'endTime': end_time,
                                      'locationId': location_id,
                                      'calendarId': calendar_id
                                  })

        return [CalendarEventDTO.model_validate(event) for event in result["events"]]
    
    async def get_blocked_slots(self, start_time: str, end_time: str, location_id: str, calendar_id: str) -> List[CalendarEventDTO]:
        result = await self.request('get',
                                  endpoint='/calendars/blocked-slots',
                                  params={
                                      'startTime': start_time,
                                      'endTime': end_time,
                                      'locationId': location_id,
                                      'calendarId': calendar_id
                                  })
        return [CalendarEventDTO.model_validate(event) for event in result["events"]]

    async def update_calendar(self, data: CalendarUpdateDTO = None, calendar_id: str = None):
        result = await self.request('put', f'/calendars/{calendar_id}', data)
        return CalendarDTO.model_validate(result)
    
    async def get_calendar(self, calendar_id: str = None):
        return await self.request('get', f'/calendars/{calendar_id}')
    
    async def delete_calendar(self, calendar_id: str = None):
        return await self.request('delete', f'/calendars/{calendar_id}')
    
    async def get_appointment(self, event_id: str = None):
        return await self.request('get', f'/calendars/events/appointments/{event_id}')
    
    async def edit_appointment(self, data: AppointmentEditSchema = None, event_id: str = None):
        return await self.request('put', f'/calendars/events/appointments/{event_id}', data)
    
    async def create_appointment(self, data: AppointmentCreateSchema = None):
        return await self.request('post', '/calendars/events/appointments', data)
    
    async def create_block_slot(self, data: BlockSlotCreateSchema = None):
        return await self.request('post', '/calendars/events/block-slots', data)
    
    async def edit_block_slot(self, data: BlockSlotEditSchema = None, event_id: str = None):
        return await self.request('put', f'/calendars/events/block-slots/{event_id}', data)
    
    async def delete_event(self, data: DeleteAppointmentSchema = None, event_id: str = None):
        return await self.request('delete', f'/calendars/events/{event_id}', data)
    
    async def get_calendar_resource(self, resource_type: str = None, _id: str = None):
        return await self.request('get', f'/calendars/resources/{resource_type}/{_id}')
    
    async def update_calendar_resource(self, data: UpdateCalendarResourceDTO = None, resource_type: str = None, _id: str = None):
        return await self.request('put', f'/calendars/resources/{resource_type}/{_id}', data)
    
    async def delete_calendar_resource(self, resource_type: str = None, _id: str = None):
        return await self.request('delete', f'/calendars/resources/{resource_type}/{_id}')
    
    async def fetch_calendar_resources(self, resource_type: str = None):
        return await self.request('get', f'/calendars/resources/{resource_type}')

    @icontract.require(lambda resource_type: resource_type in ['equipments', 'rooms'])
    async def create_calendar_resource(self, data: CreateCalendarResourceDTO = None, resource_type: str = None):
        return await self.request('post', f'/calendars/resources/{resource_type}', data)
    
    async def get_calendars(self):
        return await self.request('get', '/calendars/')
    
    async def create_calendar(self, data: CalendarCreateDTO = None):
        return await self.request('post', '/calendars/', data)


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
