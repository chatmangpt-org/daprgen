from typing import List, Optional
from datetime import datetime
from uuid import uuid4

from icontract import require, ensure

from daprgen.prototypes.calendar.models import AppointmentRequest, AppointmentResponse
from daprgen.prototypes.calendar.events import DomainEventPublisher, AppointmentCreated, AppointmentUpdated, AppointmentDeleted
from daprgen.prototypes.calendar.repository import InMemoryAppointmentRepository, GoHighLevelAppointmentRepository


class Appointment:
    def __init__(self, repository, event_publisher: DomainEventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher

    @require(lambda self, request: request.startTime < request.endTime, "Start time must be before end time")
    @require(lambda self, request: not self._is_overlapping(request.startTime, request.endTime),
             "Appointment times are overlapping with an existing appointment")
    @ensure(lambda result: result.id is not None, "Created appointment must have an ID")
    async def create(self, request: AppointmentRequest) -> AppointmentResponse:
        appointment_id = str(uuid4())
        appointment_data = request.dict()
        appointment_data["id"] = appointment_id
        appointment_response = AppointmentResponse(**appointment_data)

        await self.repository.create(appointment_response)
        self.event_publisher.publish(AppointmentCreated(appointment_response))
        return appointment_response

    async def get(self, appointment_id: str) -> AppointmentResponse:
        return await self.repository.get(appointment_id)

    @require(lambda self, appointment_id, request: request.startTime < request.endTime,
             "Start time must be before end time")
    @require(lambda self, appointment_id, request: not self._is_overlapping(request.startTime, request.endTime,
                                                                            exclude_id=appointment_id),
             "Appointment times are overlapping with an existing appointment")
    async def update(self, appointment_id: str, request: AppointmentRequest) -> AppointmentResponse:
        existing_appointment = await self.repository.get(appointment_id)

        updated_data = request.dict()
        updated_data["id"] = appointment_id
        updated_appointment = AppointmentResponse(**updated_data)

        await self.repository.update(appointment_id, updated_appointment)
        self.event_publisher.publish(AppointmentUpdated(updated_appointment))
        return updated_appointment

    async def delete(self, appointment_id: str) -> None:
        appointment = await self.repository.get(appointment_id)
        await self.repository.delete(appointment_id)
        self.event_publisher.publish(AppointmentDeleted(appointment))

    async def list(self) -> List[AppointmentResponse]:
        return await self.repository.list()

    def _is_overlapping(self, start_time: datetime, end_time: datetime, exclude_id: Optional[str] = None) -> bool:
        appointments = self.repository.appointments.values()
        for appointment in appointments:
            if exclude_id and appointment.id == exclude_id:
                continue
            if start_time < appointment.endTime and end_time > appointment.startTime:
                return True
        return False


class SimpleEventPublisher(DomainEventPublisher):
    def publish(self, event: DomainEventPublisher):
        print(f"Event published: {event}")


async def main(use_in_memory: bool = True):
    if use_in_memory:
        repository = InMemoryAppointmentRepository()
    else:
        repository = GoHighLevelAppointmentRepository()

    event_publisher = SimpleEventPublisher()
    appointment_service = Appointment(repository, event_publisher)

    # Create a new appointment
    appointment_request = AppointmentRequest(
        calendarId="CVokAlI8fgw4WYWoCtQz",
        locationId="C2QujeCh8ZnC7al2InWR",
        contactId="0007BWpSzSwfiuSl0tR2",
        startTime=datetime(2021, 6, 23, 3, 30),
        endTime=datetime(2021, 6, 23, 4, 30),
        title="Test Event",
        appointmentStatus="new",
        assignedUserId="0007BWpSzSwfiuSl0tR2",
        address="Zoom",
        ignoreDateRange=False,
        toNotify=False
    )

    created_appointment = await appointment_service.create(appointment_request)
    print(f"Created appointment: {created_appointment}")

    # Retrieve the created appointment
    retrieved_appointment = await appointment_service.get(created_appointment.id)
    print(f"Retrieved appointment: {retrieved_appointment}")

    # Update the appointment
    appointment_request.title = "Updated Test Event"
    updated_appointment = await appointment_service.update(created_appointment.id, appointment_request)
    print(f"Updated appointment: {updated_appointment}")

    # List all appointments
    appointments = await appointment_service.list()
    print(f"All appointments: {appointments}")

    # Delete the appointment
    await appointment_service.delete(created_appointment.id)
    print(f"Deleted appointment with ID: {created_appointment.id}")

    # List all appointments after deletion
    appointments = await appointment_service.list()
    print(f"All appointments after deletion: {appointments}")


# Run the main function if this module is executed directly
if __name__ == "__main__":
    import asyncio

    # Change to False to test with GoHighLevelAppointmentRepository
    asyncio.run(main(use_in_memory=True))
