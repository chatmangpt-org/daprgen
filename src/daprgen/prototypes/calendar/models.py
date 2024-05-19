from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AppointmentRequest(BaseModel):
    calendarId: str = Field(..., description="Calendar Id", example="CVokAlI8fgw4WYWoCtQz")
    locationId: str = Field(..., description="Location Id", example="C2QujeCh8ZnC7al2InWR")
    contactId: str = Field(..., description="Contact Id", example="0007BWpSzSwfiuSl0tR2")
    startTime: datetime = Field(..., description="Start Time", example="2021-06-23T03:30:00+05:30")
    endTime: Optional[datetime] = Field(None, description="End Time", example="2021-06-23T04:30:00+05:30")
    title: Optional[str] = Field(None, description="Title", example="Test Event")
    appointmentStatus: str = Field(..., description="Appointment Status", example="new",
                                   enum=["new", "confirmed", "cancelled", "showed", "noshow", "invalid"])
    assignedUserId: Optional[str] = Field(None, description="Assigned User Id", example="0007BWpSzSwfiuSl0tR2")
    address: Optional[str] = Field(None, description="Appointment Address", example="Zoom")
    ignoreDateRange: bool = Field(..., description="If set to true, the minimum scheduling notice and date range would be ignored", example=False)
    toNotify: bool = Field(..., description="If set to false, the automations will not run", example=False)

class AppointmentResponse(BaseModel):
    calendarId: str = Field(..., description="Calendar Id", example="CVokAlI8fgw4WYWoCtQz")
    locationId: str = Field(..., description="Location Id", example="C2QujeCh8ZnC7al2InWR")
    contactId: str = Field(..., description="Contact Id", example="0007BWpSzSwfiuSl0tR2")
    startTime: datetime = Field(..., description="Start Time", example="2021-06-23T03:30:00+05:30")
    endTime: datetime = Field(..., description="End Time", example="2021-06-23T04:30:00+05:30")
    title: str = Field(..., description="Title", example="Test Event")
    appointmentStatus: str = Field(..., description="Appointment Status", example="new")
    assignedUserId: str = Field(..., description="Assigned User Id", example="0007BWpSzSwfiuSl0tR2")
    address: str = Field(..., description="Appointment Address", example="Zoom")
    id: str = Field(..., description="Appointment Id", example="0TkCdp9PfvLeWKYRRvIz")
