import inject
import asyncio
from uuid import uuid4

from daprgen.prototypes.calendar.models import AppointmentResponse
from daprgen.prototypes.calendar.repository import GoHighLevelAppointmentRepository, InMemoryAppointmentRepository





def configure(binder):
    binder.bind(httpx.AsyncClient, httpx.AsyncClient())
    binder.bind(GoHighLevelAppointmentRepository, GoHighLevelAppointmentRepository(client=httpx.AsyncClient()))
    binder.bind(InMemoryAppointmentRepository, InMemoryAppointmentRepository())


async def main():
    # Setup dependency injection
    inject.configure(configure)

    # Inject the GoHighLevelAppointmentRepository
    repository = inject.instance(GoHighLevelAppointmentRepository)

    # Sample appointment response
    sample_appointment_response = AppointmentResponse(
        calendarId=str(uuid4()),
        locationId=str(uuid4()),
        contactId=str(uuid4()),
        startTime="2021-06-23T03:30:00+05:30",
        endTime="2021-06-23T04:30:00+05:30",
        title="Test Event",
        appointmentStatus="new",
        assignedUserId=str(uuid4()),
        address="Zoom",
        id=str(uuid4())
    )

    # Create appointment
    await repository.create(sample_appointment_response)
    print(f"Created appointment: {sample_appointment_response}")

    # Get appointment
    fetched_appointment = await repository.get(sample_appointment_response.id)
    print(f"Fetched appointment: {fetched_appointment}")

    # Update appointment
    sample_appointment_response.title = "Updated Test Event"
    await repository.update(sample_appointment_response.id, sample_appointment_response)
    print(f"Updated appointment: {sample_appointment_response}")

    # List appointments
    appointments = await repository.list()
    print(f"List of appointments: {appointments}")

    # Delete appointment
    await repository.delete(sample_appointment_response.id)
    print(f"Deleted appointment with ID: {sample_appointment_response.id}")


if __name__ == "__main__":
    asyncio.run(main())
