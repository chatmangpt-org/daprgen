import inject
import httpx
import asyncio

class AppointmentService:
    def __init__(self, base_url, auth_token, version):
        self.base_url = base_url
        self.auth_token = auth_token
        self.version = version

    async def create_appointment(self, appointment_data):
        async with httpx.AsyncClient() as client:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Version': self.version,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = await client.post(
                f"{self.base_url}/calendars/events/appointments",
                json=appointment_data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

# Create an optional configuration.
def my_config(binder):
    binder.bind(AppointmentService, AppointmentService(
        base_url="https://stoplight.io/mocks/highlevel/integrations/39582850",
        auth_token="9c48df2694a849b6089f9d0d3513efe",
        version="2021-04-15"
    ))

# Configure a shared injector.
inject.configure(my_config)

# Example function using the injected AppointmentService
@inject.params(service=AppointmentService)
async def create_test_appointment(service=None):
    appointment_data = {
        "calendarId": "CVokAlI8fgw4WYWoCtQz",
        "locationId": "C2QujeCh8ZnC7al2InWR",
        "contactId": "0007BWpSzSwfiuSl0tR2",
        "startTime": "2021-06-23T03:30:00+05:30",
        "endTime": "2021-06-23T04:30:00+05:30",
        "title": "Test Event",
        "appointmentStatus": "new",
        "assignedUserId": "0007BWpSzSwfiuSl0tR2",
        "address": "Zoom",
        "ignoreDateRange": False,
        "toNotify": False
    }
    return await service.create_appointment(appointment_data)

# Main function to run the example
async def main():
    result = await create_test_appointment()
    print(result)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
