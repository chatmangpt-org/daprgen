from datetime import datetime


from daprgen.prototypes.calendar.ghl_calendar_models import *
import factory
from factory import Faker, SubFactory
from factory.fuzzy import FuzzyChoice
import random


class BadRequestDTOFactory(factory.Factory):
    class Meta:
        model = BadRequestDTO

    statusCode = Faker('pyfloat', positive=True)
    message = Faker('sentence')


class UnauthorizedDTOFactory(factory.Factory):
    class Meta:
        model = UnauthorizedDTO

    statusCode = Faker('pyfloat', positive=True)
    message = Faker('sentence')
    error = Faker('word')


class GroupSchemaFactory(factory.Factory):
    class Meta:
        model = GroupSchema

    id = Faker('uuid4')
    locationId = Faker('uuid4')
    name = Faker('company')
    isActive = Faker('boolean')
    description = Faker('paragraph')
    slug = Faker('slug')


class GroupsGetSuccessfulResponseDTOFactory(factory.Factory):
    class Meta:
        model = GroupsGetSuccessfulResponseDTO

    groups = factory.List([SubFactory(GroupSchemaFactory) for _ in range(3)])


class ValidateGroupSlugPostBodyFactory(factory.Factory):
    class Meta:
        model = ValidateGroupSlugPostBody

    locationId = Faker('uuid4')
    slug = Faker('slug')


class ValidateGroupSlugSuccessResponseDTOFactory(factory.Factory):
    class Meta:
        model = ValidateGroupSlugSuccessResponseDTO

    available = Faker('boolean')


class GroupDTOFactory(factory.Factory):
    class Meta:
        model = GroupDTO

    id = Faker('uuid4')
    locationId = Faker('uuid4')
    name = Faker('company')
    description = Faker('paragraph')
    slug = Faker('slug')
    isActive = Faker('boolean')
    dateAdded = "2024-05-18T21:40:33.783945-07:00"
    dateUpdated = "2024-05-18T21:40:33.783945-07:00"


class GroupCreateSuccessfulResponseDTOFactory(factory.Factory):
    class Meta:
        model = GroupCreateSuccessfulResponseDTO

    group = SubFactory(GroupDTOFactory)


class GroupSuccessfulResponseDTOFactory(factory.Factory):
    class Meta:
        model = GroupSuccessfulResponseDTO

    success = Faker('boolean')


class GroupStatusUpdateParamsFactory(factory.Factory):
    class Meta:
        model = GroupStatusUpdateParams

    isActive = Faker('boolean')


class GroupUpdateDTOFactory(factory.Factory):
    class Meta:
        model = GroupUpdateDTO

    id = Faker('uuid4')
    name = Faker('company')
    description = Faker('paragraph')
    slug = Faker('slug')


class CalendarEventDTOFactory(factory.Factory):
    class Meta:
        model = CalendarEventDTO

    id = Faker('uuid4')
    address = Faker('address')
    title = Faker('sentence')
    calendarId = Faker('uuid4')
    locationId = Faker('uuid4')
    contactId = Faker('uuid4')
    groupId = Faker('uuid4')
    appointmentStatus = FuzzyChoice(['Scheduled', 'Cancelled', 'Completed'])
    assignedUserId = Faker('uuid4')
    users = factory.List([Faker('uuid4') for _ in range(3)])
    notes = Faker('text')
    startTime = "2024-05-18T21:40:33.783945-07:00"
    endTime = "2024-05-18T21:40:33.783945-07:00"
    dateAdded = "2024-05-18T21:40:33.783945-07:00"
    dateUpdated = "2024-05-18T21:40:33.783945-07:00"


class GetCalendarEventsSuccessfulResponseDTOFactory(factory.Factory):
    class Meta:
        model = GetCalendarEventsSuccessfulResponseDTO

    events = factory.List([SubFactory(CalendarEventDTOFactory) for _ in range(3)])


class SlotsSchemaFactory(factory.Factory):
    class Meta:
        model = SlotsSchema

    slots = factory.List([{'start': "2024-05-18T21:40:33.783945-07:00", 'end': "2024-05-18T21:40:33.783945-07:00"} for _ in range(3)])


class GetSlotsSuccessfulResponseDtoFactory(factory.Factory):
    class Meta:
        model = GetSlotsSuccessfulResponseDto

    _dates_ = factory.List(["2024-05-18T21:40:33.783945-07:00" for _ in range(3)])


class CalendarNotificationFactory(factory.Factory):
    class Meta:
        model = CalendarNotification

    type = Faker('word')
    shouldSendToContact = Faker('boolean')
    shouldSendToGuest = Faker('boolean')
    shouldSendToUser = Faker('boolean')
    shouldSendToSelectedUsers = Faker('boolean')
    selectedUsers = Faker('uuid4')


class TeamMemberFactory(factory.Factory):
    class Meta:
        model = TeamMember

    userId = Faker('uuid4')
    priority = Faker('pyfloat', positive=True, max_value=1)
    meetingLocationType = Faker('word')
    meetingLocation = Faker('address')
    isPrimary = Faker('boolean')


class HourFactory(factory.Factory):
    class Meta:
        model = Hour

    openHour = Faker('pyfloat', positive=True, max_value=23)
    openMinute = Faker('pyfloat', positive=True, max_value=59)
    closeHour = Faker('pyfloat', positive=True, max_value=23)
    closeMinute = Faker('pyfloat', positive=True, max_value=59)


class OpenHourFactory(factory.Factory):
    class Meta:
        model = OpenHour

    daysOfTheWeek = factory.List([random.randint(1, 7) for _ in range(3)])
    hours = factory.List([SubFactory(HourFactory) for _ in range(3)])


class RecurringFactory(factory.Factory):
    class Meta:
        model = Recurring


class AvailabilityFactory(factory.Factory):
    class Meta:
        model = Availability

    id = Faker('uuid4')
    date = Faker('date')
    hours = factory.List([SubFactory(HourFactory) for _ in range(3)])
    deleted = Faker('boolean')


class CalendarDTOFactory(factory.Factory):
    class Meta:
        model = CalendarDTO

    notifications = factory.List([SubFactory(CalendarNotificationFactory) for _ in range(3)])
    locationId = Faker('uuid4')
    groupId = Faker('uuid4')
    teamMembers = factory.List([SubFactory(TeamMemberFactory) for _ in range(3)])
    eventType = Faker('word')
    name = Faker('company')
    description = Faker('paragraph')
    slug = Faker('slug')
    widgetSlug = Faker('slug')
    calendarType = Faker('word')
    widgetType = Faker('word')
    eventTitle = Faker('sentence')
    eventColor = Faker('color')
    meetingLocation = Faker('address')
    slotDuration = Faker('pyfloat', positive=True)
    preBufferUnit = Faker('word')
    slotInterval = Faker('pyfloat', positive=True)
    slotBuffer = Faker('pyfloat', positive=True)
    preBuffer = Faker('pyfloat', positive=True)
    appoinmentPerSlot = Faker('pyfloat', positive=True)
    appoinmentPerDay = Faker('pyfloat', positive=True)
    openHours = factory.List([SubFactory(OpenHourFactory) for _ in range(3)])
    enableRecurring = Faker('boolean')
    recurring = SubFactory(RecurringFactory)
    formId = Faker('uuid4')
    stickyContact = Faker('boolean')
    isLivePaymentMode = Faker('boolean')
    autoConfirm = Faker('boolean')
    shouldSendAlertEmailsToAssignedMember = Faker('boolean')
    alertEmail = Faker('email')
    googleInvitationEmails = Faker('boolean')
    allowReschedule = Faker('boolean')
    allowCancellation = Faker('boolean')
    shouldAssignContactToTeamMember = Faker('boolean')
    shouldSkipAssigningContactForExisting = Faker('boolean')
    notes = Faker('text')
    pixelId = Faker('uuid4')
    formSubmitType = Faker('word')
    formSubmitRedirectURL = Faker('url')
    formSubmitThanksMessage = Faker('sentence')
    availabilityType = Faker('random_int', min=0, max=1)
    availabilities = factory.List([SubFactory(AvailabilityFactory) for _ in range(3)])
    guestType = Faker('word')
    consentLabel = Faker('sentence')
    calendarCoverImage = Faker('image_url')
    id = Faker('uuid4')


class CalendarsGetSuccessfulResponseDTOFactory(factory.Factory):
    class Meta:
        model = CalendarsGetSuccessfulResponseDTO

    calendars = factory.List([SubFactory(CalendarDTOFactory) for _ in range(3)])


class CalendarCreateDTOFactory(factory.Factory):
    class Meta:
        model = CalendarCreateDTO

    notifications = factory.List([SubFactory(CalendarNotificationFactory) for _ in range(3)])
    locationId = Faker('uuid4')
    groupId = Faker('uuid4')
    teamMembers = factory.List([SubFactory(TeamMemberFactory) for _ in range(3)])
    eventType = Faker('word')
    name = Faker('company')
    description = Faker('paragraph')
    slug = Faker('slug')
    widgetSlug = Faker('slug')
    calendarType = Faker('word')
    widgetType = Faker('word')
    eventTitle = Faker('sentence')
    eventColor = Faker('color')
    meetingLocation = Faker('address')
    slotDuration = Faker('pyfloat', positive=True)
    preBufferUnit = Faker('word')
    slotInterval = Faker('pyfloat', positive=True)
    slotBuffer = Faker('pyfloat', positive=True)
    preBuffer = Faker('pyfloat', positive=True)
    appoinmentPerSlot = Faker('pyfloat', positive=True)
    appoinmentPerDay = Faker('pyfloat', positive=True)
    openHours = factory.List([SubFactory(OpenHourFactory) for _ in range(3)])
    enableRecurring = Faker('boolean')
    recurring = SubFactory(RecurringFactory)
    formId = Faker('uuid4')
    stickyContact = Faker('boolean')
    isLivePaymentMode = Faker('boolean')
    autoConfirm = Faker('boolean')
    shouldSendAlertEmailsToAssignedMember = Faker('boolean')
    alertEmail = Faker('email')
    googleInvitationEmails = Faker('boolean')
    allowReschedule = Faker('boolean')
    allowCancellation = Faker('boolean')
    shouldAssignContactToTeamMember = Faker('boolean')
    shouldSkipAssigningContactForExisting = Faker('boolean')
    notes = Faker('text')
    pixelId = Faker('uuid4')
    formSubmitType = Faker('word')
    formSubmitRedirectURL = Faker('url')
    formSubmitThanksMessage = Faker('sentence')
    availabilityType = Faker('random_int', min=0, max=1)
    availabilities = factory.List([SubFactory(AvailabilityFactory) for _ in range(3)])
    guestType = Faker('word')
    consentLabel = Faker('sentence')
    calendarCoverImage = Faker('image_url')
    id = Faker('uuid4')


class CalendarByIdSuccessfulResponseDTOFactory(factory.Factory):
    class Meta:
        model = CalendarByIdSuccessfulResponseDTO

    calendar = SubFactory(CalendarDTOFactory)


class CalendarUpdateDTOFactory(factory.Factory):
    class Meta:
        model = CalendarUpdateDTO

    notifications = factory.List([SubFactory(CalendarNotificationFactory) for _ in range(3)])
    groupId = Faker('uuid4')
    teamMembers = factory.List([SubFactory(TeamMemberFactory) for _ in range(3)])
    eventType = Faker('word')
    name = Faker('company')
    description = Faker('paragraph')
    slug = Faker('slug')
    widgetSlug = Faker('slug')
    widgetType = Faker('word')
    eventTitle = Faker('sentence')
    eventColor = Faker('color')
    meetingLocation = Faker('address')
    slotDuration = Faker('pyfloat', positive=True)
    preBufferUnit = Faker('word')
    slotInterval = Faker('pyfloat', positive=True)
    slotBuffer = Faker('pyfloat', positive=True)
    preBuffer = Faker('pyfloat', positive=True)
    appoinmentPerSlot = Faker('pyfloat', positive=True)
    appoinmentPerDay = Faker('pyfloat', positive=True)
    openHours = factory.List([SubFactory(OpenHourFactory) for _ in range(3)])
    enableRecurring = Faker('boolean')
    recurring = SubFactory(RecurringFactory)
    formId = Faker('uuid4')
    stickyContact = Faker('boolean')
    isLivePaymentMode = Faker('boolean')
    autoConfirm = Faker('boolean')
    shouldSendAlertEmailsToAssignedMember = Faker('boolean')
    alertEmail = Faker('email')
    googleInvitationEmails = Faker('boolean')
    allowReschedule = Faker('boolean')
    allowCancellation = Faker('boolean')
    shouldAssignContactToTeamMember = Faker('boolean')
    shouldSkipAssigningContactForExisting = Faker('boolean')
    notes = Faker('text')
    pixelId = Faker('uuid4')
    formSubmitType = Faker('word')
    formSubmitRedirectURL = Faker('url')
    formSubmitThanksMessage = Faker('sentence')
    availabilityType = Faker('random_int', min=0, max=1)
    availabilities = factory.List([SubFactory(AvailabilityFactory) for _ in range(3)])
    guestType = Faker('word')
    consentLabel = Faker('sentence')
    calendarCoverImage = Faker('image_url')


class CalendarDeleteSuccessfulResponseDTOFactory(factory.Factory):
    class Meta:
        model = CalendarDeleteSuccessfulResponseDTO

    success = Faker('boolean')


class GetCalendarEventSuccessfulResponseDTOFactory(factory.Factory):
    class Meta:
        model = GetCalendarEventSuccessfulResponseDTO

    event = SubFactory(CalendarEventDTOFactory)


class AppointmentCreateSchemaFactory(factory.Factory):
    class Meta:
        model = AppointmentCreateSchema

    calendarId = Faker('uuid4')
    locationId = Faker('uuid4')
    contactId = Faker('uuid4')
    startTime = "2024-05-18T21:40:33.783945-07:00"
    endTime = "2024-05-18T21:40:33.783945-07:00"
    title = Faker('sentence')
    appointmentStatus = FuzzyChoice(['Scheduled', 'Cancelled', 'Completed'])
    assignedUserId = Faker('uuid4')
    address = Faker('address')
    ignoreDateRange = Faker('boolean')
    toNotify = Faker('boolean')


class AppointmentSchemaResponseFactory(factory.Factory):
    class Meta:
        model = AppointmentSchemaResponse

    calendarId = Faker('uuid4')
    locationId = Faker('uuid4')
    contactId = Faker('uuid4')
    startTime = "2024-05-18T21:40:33.783945-07:00"
    endTime = "2024-05-18T21:40:33.783945-07:00"
    title = Faker('sentence')
    appointmentStatus = FuzzyChoice(['Scheduled', 'Cancelled', 'Completed'])
    assignedUserId = Faker('uuid4')
    address = Faker('address')
    id = Faker('uuid4')


class AppointmentEditSchemaFactory(factory.Factory):
    class Meta:
        model = AppointmentEditSchema

    calendarId = Faker('uuid4')
    startTime = "2024-05-18T21:40:33.783945-07:00"
    endTime = "2024-05-18T21:40:33.783945-07:00"
    title = Faker('sentence')
    appointmentStatus = FuzzyChoice(['Scheduled', 'Cancelled', 'Completed'])
    address = Faker('address')
    ignoreDateRange = Faker('boolean')
    toNotify = Faker('boolean')


class BlockSlotCreateSchemaFactory(factory.Factory):
    class Meta:
        model = BlockSlotCreateSchema

    calendarId = Faker('uuid4')
    locationId = Faker('uuid4')
    startTime = "2024-05-18T21:40:33.783945-07:00"
    endTime = "2024-05-18T21:40:33.783945-07:00"
    title = Faker('sentence')
    assignedUserId = Faker('uuid4')


class CreateBookedSlotSuccessfulResponseDtoFactory(factory.Factory):
    class Meta:
        model = CreateBookedSlotSuccessfulResponseDto

    id = Faker('uuid4')
    locationId = Faker('uuid4')
    title = Faker('sentence')
    startTime = "2024-05-18T21:40:33.783945-07:00"
    endTime = "2024-05-18T21:40:33.783945-07:00"
    calendarId = Faker('uuid4')
    assignedUserId = Faker('uuid4')


class BlockSlotEditSchemaFactory(factory.Factory):
    class Meta:
        model = BlockSlotEditSchema

    calendarId = Faker('uuid4')
    startTime = "2024-05-18T21:40:33.783945-07:00"
    endTime = "2024-05-18T21:40:33.783945-07:00"
    title = Faker('sentence')
    assignedUserId = Faker('uuid4')


class DeleteAppointmentSchemaFactory(factory.Factory):
    class Meta:
        model = DeleteAppointmentSchema

    eventId = Faker('uuid4')


class DeleteEventSuccessfulResponseDtoFactory(factory.Factory):
    class Meta:
        model = DeleteEventSuccessfulResponseDto

    succeeded = Faker('boolean')


class UpdateCalendarResourceDTOFactory(factory.Factory):
    class Meta:
        model = UpdateCalendarResourceDTO

    locationId = Faker('uuid4')
    name = Faker('company')
    description = Faker('paragraph')
    quantity = Faker('pyfloat', positive=True)
    outOfService = Faker('pyfloat', positive=True)
    capacity = Faker('pyfloat', positive=True)
    calendarIds = factory.List([Faker('uuid4') for _ in range(3)])
    isActive = Faker('boolean')
    deleted = Faker('boolean')


class CreateCalendarResourceDTOFactory(factory.Factory):
    class Meta:
        model = CreateCalendarResourceDTO

    locationId = Faker('uuid4')
    name = Faker('company')
    description = Faker('paragraph')
    quantity = Faker('pyfloat', positive=True)
    outOfService = Faker('pyfloat', positive=True)
    capacity = Faker('pyfloat', positive=True)
    calendarIds = factory.List([Faker('uuid4') for _ in range(3)])
    isActive = Faker('boolean')
