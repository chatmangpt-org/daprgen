from typing import List, Optional
import httpx
from uuid import uuid4
import asyncio


from daprgen.prototypes.calendar.models import AppointmentResponse


class GoHighLevelAppointmentRepository:
    BASE_URL = "https://stoplight.io/mocks/highlevel/integrations/39582850/calendars/events/appointments"
    HEADERS = {
        "Authorization": "Bearer 9c48df2694a849b6089f9d0d3513efe",
        "Version": "2021-04-15",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def create(self, appointment: AppointmentResponse) -> None:
        response = await self.client.post(self.BASE_URL, headers=self.HEADERS, json=appointment.model_dump_json())
        response.raise_for_status()

    async def get(self, appointment_id: str) -> AppointmentResponse:
        response = await self.client.get(f"{self.BASE_URL}/{appointment_id}", headers=self.HEADERS)
        response.raise_for_status()
        return AppointmentResponse(**response.json())

    async def update(self, appointment_id: str, appointment: AppointmentResponse) -> None:
        response = await self.client.put(f"{self.BASE_URL}/{appointment_id}", headers=self.HEADERS,
                                         json=appointment.model_dump_json())
        response.raise_for_status()

    async def delete(self, appointment_id: str) -> None:
        response = await self.client.delete(f"{self.BASE_URL}/{appointment_id}", headers=self.HEADERS)
        response.raise_for_status()

    async def list(self) -> List[AppointmentResponse]:
        response = await self.client.get(self.BASE_URL, headers=self.HEADERS)
        response.raise_for_status()
        return [AppointmentResponse(**appointment) for appointment in response.json()]

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()


class InMemoryAppointmentRepository:
    def __init__(self):
        self.appointments: dict[str, AppointmentResponse] = {}

    async def create(self, appointment: AppointmentResponse) -> None:
        self.appointments[appointment.id] = appointment

    async def get(self, appointment_id: str) -> AppointmentResponse:
        return self.appointments[appointment_id]

    async def update(self, appointment_id: str, appointment: AppointmentResponse) -> None:
        self.appointments[appointment_id] = appointment

    async def delete(self, appointment_id: str) -> None:
        del self.appointments[appointment_id]

    async def list(self) -> List[AppointmentResponse]:
        return list(self.appointments.values())
