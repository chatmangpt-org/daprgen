from pydantic import BaseModel
from typing import Optional, List, Any, Dict


class BadRequestDTO(BaseModel):
    statusCode: Optional[float] = None
    message: Optional[str] = None


class UnauthorizedDTO(BaseModel):
    statusCode: Optional[float] = None
    message: Optional[str] = None
    error: Optional[str] = None


class GroupSchema(BaseModel):
    id: Optional[str] = None
    locationId: Optional[str] = None
    name: Optional[str] = None
    isActive: Optional[bool] = None
    description: Optional[str] = None
    slug: Optional[str] = None


class GroupsGetSuccessfulResponseDTO(BaseModel):
    groups: Optional[List[GroupSchema]] = None


class ValidateGroupSlugPostBody(BaseModel):
    locationId: Optional[str] = None
    slug: Optional[str] = None


class ValidateGroupSlugSuccessResponseDTO(BaseModel):
    available: Optional[bool] = None


class GroupDTO(BaseModel):
    id: Optional[str] = None
    locationId: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    isActive: Optional[bool] = None
    dateAdded: Optional[str] = None
    dateUpdated: Optional[str] = None


class GroupCreateSuccessfulResponseDTO(BaseModel):
    group: Optional[GroupDTO] = None


class GroupSuccessfulResponseDTO(BaseModel):
    success: Optional[bool] = None


class GroupStatusUpdateParams(BaseModel):
    isActive: Optional[bool] = None


class GroupUpdateDTO(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None


class CalendarEventDTO(BaseModel):
    id: Optional[str] = None
    address: Optional[str] = None
    title: Optional[str] = None
    calendarId: Optional[str] = None
    locationId: Optional[str] = None
    contactId: Optional[str] = None
    groupId: Optional[str] = None
    appointmentStatus: Optional[str] = None
    assignedUserId: Optional[str] = None
    users: Optional[List[str]] = None
    notes: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    dateAdded: Optional[str] = None
    dateUpdated: Optional[str] = None


class GetCalendarEventsSuccessfulResponseDTO(BaseModel):
    events: Optional[List[CalendarEventDTO]] = None


class SlotsSchema(BaseModel):
    slots: Optional[List[Dict[str, Any]]] = None


class GetSlotsSuccessfulResponseDto(BaseModel):
    _dates_: Optional[Any] = None


class CalendarNotification(BaseModel):
    type: Optional[str] = ""
    shouldSendToContact: Optional[bool] = None
    shouldSendToGuest: Optional[bool] = None
    shouldSendToUser: Optional[bool] = None
    shouldSendToSelectedUsers: Optional[bool] = None
    selectedUsers: Optional[str] = None


class TeamMember(BaseModel):
    userId: Optional[str] = None
    priority: Optional[float] = 0.5
    meetingLocationType: Optional[str] = None
    meetingLocation: Optional[str] = None
    isPrimary: Optional[bool] = None


class Hour(BaseModel):
    openHour: Optional[float] = None
    openMinute: Optional[float] = None
    closeHour: Optional[float] = None
    closeMinute: Optional[float] = None


class OpenHour(BaseModel):
    daysOfTheWeek: Optional[List[int]] = None
    hours: Optional[List[Hour]] = None


class Recurring(BaseModel):
    pass


class Availability(BaseModel):
    id: Optional[str] = None
    date: Optional[str] = None
    hours: Optional[List[Hour]] = None
    deleted: Optional[bool] = False


class CalendarDTO(BaseModel):
    notifications: Optional[List[CalendarNotification]] = None
    locationId: Optional[str] = None
    groupId: Optional[str] = None
    teamMembers: Optional[List[TeamMember]] = None
    eventType: Optional[str] = ""
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    widgetSlug: Optional[str] = None
    calendarType: Optional[str] = None
    widgetType: Optional[str] = ""
    eventTitle: Optional[str] = ""
    eventColor: Optional[str] = ""
    meetingLocation: Optional[str] = None
    slotDuration: Optional[float] = 30
    preBufferUnit: Optional[str] = None
    slotInterval: Optional[float] = 30
    slotBuffer: Optional[float] = None
    preBuffer: Optional[float] = None
    appoinmentPerSlot: Optional[float] = 1
    appoinmentPerDay: Optional[float] = None
    openHours: Optional[List[OpenHour]] = None
    enableRecurring: Optional[bool] = None
    recurring: Optional[Recurring] = None
    formId: Optional[str] = None
    stickyContact: Optional[bool] = None
    isLivePaymentMode: Optional[bool] = None
    autoConfirm: Optional[bool] = True
    shouldSendAlertEmailsToAssignedMember: Optional[bool] = None
    alertEmail: Optional[str] = None
    googleInvitationEmails: Optional[bool] = False
    allowReschedule: Optional[bool] = True
    allowCancellation: Optional[bool] = True
    shouldAssignContactToTeamMember: Optional[bool] = None
    shouldSkipAssigningContactForExisting: Optional[bool] = None
    notes: Optional[str] = None
    pixelId: Optional[str] = None
    formSubmitType: Optional[str] = ""
    formSubmitRedirectURL: Optional[str] = None
    formSubmitThanksMessage: Optional[str] = None
    availabilityType: Optional[int] = 0
    availabilities: Optional[List[Availability]] = None
    guestType: Optional[str] = None
    consentLabel: Optional[str] = None
    calendarCoverImage: Optional[str] = None
    id: Optional[str] = None


class CalendarsGetSuccessfulResponseDTO(BaseModel):
    calendars: Optional[List[CalendarDTO]] = None


class CalendarCreateDTO(BaseModel):
    notifications: Optional[List[CalendarNotification]] = None
    locationId: Optional[str] = None
    groupId: Optional[str] = None
    teamMembers: Optional[List[TeamMember]] = None
    eventType: Optional[str] = ""
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    widgetSlug: Optional[str] = None
    calendarType: Optional[str] = None
    widgetType: Optional[str] = ""
    eventTitle: Optional[str] = ""
    eventColor: Optional[str] = ""
    meetingLocation: Optional[str] = None
    slotDuration: Optional[float] = 30
    preBufferUnit: Optional[str] = None
    slotInterval: Optional[float] = 30
    slotBuffer: Optional[float] = None
    preBuffer: Optional[float] = None
    appoinmentPerSlot: Optional[float] = 1
    appoinmentPerDay: Optional[float] = None
    openHours: Optional[List[OpenHour]] = None
    enableRecurring: Optional[bool] = None
    recurring: Optional[Recurring] = None
    formId: Optional[str] = None
    stickyContact: Optional[bool] = None
    isLivePaymentMode: Optional[bool] = None
    autoConfirm: Optional[bool] = True
    shouldSendAlertEmailsToAssignedMember: Optional[bool] = None
    alertEmail: Optional[str] = None
    googleInvitationEmails: Optional[bool] = False
    allowReschedule: Optional[bool] = True
    allowCancellation: Optional[bool] = True
    shouldAssignContactToTeamMember: Optional[bool] = None
    shouldSkipAssigningContactForExisting: Optional[bool] = None
    notes: Optional[str] = None
    pixelId: Optional[str] = None
    formSubmitType: Optional[str] = ""
    formSubmitRedirectURL: Optional[str] = None
    formSubmitThanksMessage: Optional[str] = None
    availabilityType: Optional[int] = 0
    availabilities: Optional[List[Availability]] = None
    guestType: Optional[str] = None
    consentLabel: Optional[str] = None
    calendarCoverImage: Optional[str] = None


class CalendarByIdSuccessfulResponseDTO(BaseModel):
    calendar: Optional[CalendarDTO] = None


class CalendarUpdateDTO(BaseModel):
    notifications: Optional[List[CalendarNotification]] = None
    groupId: Optional[str] = None
    teamMembers: Optional[List[TeamMember]] = None
    eventType: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    widgetSlug: Optional[str] = None
    widgetType: Optional[str] = ""
    eventTitle: Optional[str] = None
    eventColor: Optional[str] = ""
    meetingLocation: Optional[str] = None
    slotDuration: Optional[float] = None
    preBufferUnit: Optional[str] = None
    slotInterval: Optional[float] = None
    slotBuffer: Optional[float] = None
    preBuffer: Optional[float] = None
    appointmentPerSlot: Optional[float] = None
    appointmentPerDay: Optional[float] = None
    openHours: Optional[List[OpenHour]] = None
    enableRecurring: Optional[bool] = None
    recurring: Optional[Recurring] = None
    formId: Optional[str] = None
    stickyContact: Optional[bool] = None
    isLivePaymentMode: Optional[bool] = None
    autoConfirm: Optional[bool] = None
    shouldSendAlertEmailsToAssignedMember: Optional[bool] = None
    alertEmail: Optional[str] = None
    googleInvitationEmails: Optional[bool] = None
    allowReschedule: Optional[bool] = None
    allowCancellation: Optional[bool] = None
    shouldAssignContactToTeamMember: Optional[bool] = None
    shouldSkipAssigningContactForExisting: Optional[bool] = None
    notes: Optional[str] = None
    pixelId: Optional[str] = None
    formSubmitType: Optional[str] = ""
    formSubmitRedirectURL: Optional[str] = None
    formSubmitThanksMessage: Optional[str] = None
    availabilityType: Optional[int] = 0
    availabilities: Optional[List[Availability]] = None
    guestType: Optional[str] = None
    consentLabel: Optional[str] = None
    calendarCoverImage: Optional[str] = None


class CalendarDeleteSuccessfulResponseDTO(BaseModel):
    success: Optional[bool] = None


class GetCalendarEventSuccessfulResponseDTO(BaseModel):
    event: Optional[CalendarEventDTO] = None


class AppointmentCreateSchema(BaseModel):
    calendarId: Optional[str] = None
    locationId: Optional[str] = None
    contactId: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    title: Optional[str] = None
    appointmentStatus: Optional[str] = None
    assignedUserId: Optional[str] = None
    address: Optional[str] = None
    ignoreDateRange: Optional[bool] = None
    toNotify: Optional[bool] = None


class AppointmentSchemaResponse(BaseModel):
    calendarId: Optional[str] = None
    locationId: Optional[str] = None
    contactId: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    title: Optional[str] = None
    appointmentStatus: Optional[str] = None
    assignedUserId: Optional[str] = None
    address: Optional[str] = None
    id: Optional[str] = None


class AppointmentEditSchema(BaseModel):
    calendarId: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    title: Optional[str] = None
    appointmentStatus: Optional[str] = None
    address: Optional[str] = None
    ignoreDateRange: Optional[bool] = None
    toNotify: Optional[bool] = None


class BlockSlotCreateSchema(BaseModel):
    calendarId: Optional[str] = None
    locationId: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    title: Optional[str] = None
    assignedUserId: Optional[str] = None


class CreateBookedSlotSuccessfulResponseDto(BaseModel):
    id: Optional[str] = None
    locationId: Optional[str] = None
    title: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    calendarId: Optional[str] = None
    assignedUserId: Optional[str] = None


class BlockSlotEditSchema(BaseModel):
    calendarId: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    title: Optional[str] = None
    assignedUserId: Optional[str] = None


class DeleteAppointmentSchema(BaseModel):
    eventId: Optional[str] = None


class DeleteEventSuccessfulResponseDto(BaseModel):
    succeeded: Optional[bool] = None


class UpdateCalendarResourceDTO(BaseModel):
    locationId: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[float] = None
    outOfService: Optional[float] = None
    capacity: Optional[float] = None
    calendarIds: Optional[List[str]] = None
    isActive: Optional[bool] = None
    deleted: Optional[bool] = None


class CreateCalendarResourceDTO(BaseModel):
    locationId: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[float] = None
    outOfService: Optional[float] = None
    capacity: Optional[float] = None
    calendarIds: Optional[List[str]] = None
    isActive: Optional[bool] = None
