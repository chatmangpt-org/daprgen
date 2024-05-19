import pytest
import vcr
from daprgen.prototypes.calendar.ghl_calendar_service import GHLCalendarService
from daprgen.prototypes.calendar.ghl_calendar_models import *

from daprgen.mocks import (GroupDTOFactory, ValidateGroupSlugPostBodyFactory, GroupUpdateDTOFactory,
                           GroupStatusUpdateParamsFactory, AppointmentCreateSchemaFactory,
                           AppointmentEditSchemaFactory, BlockSlotCreateSchemaFactory,
                           BlockSlotEditSchemaFactory, DeleteAppointmentSchemaFactory,
                           UpdateCalendarResourceDTOFactory, CreateCalendarResourceDTOFactory,
                           CalendarCreateDTOFactory, CalendarUpdateDTOFactory, CalendarEventDTOFactory)


@pytest.mark.asyncio
async def test_get_groups(service):
    response = await service.get_groups(location_id="ve9EPM428h8vShlRW1KT")
    assert response is not None
    assert isinstance(response, list)


@pytest.mark.asyncio
async def test_create_calendar_group(service):
    dto = GroupDTOFactory()
    response = await service.create_calendar_group(data=dto)
    assert response is not None


@pytest.mark.asyncio
async def test_validate_groups_slug(service):
    dto = ValidateGroupSlugPostBodyFactory()
    response = await service.validate_groups_slug(data=dto)
    assert response is not None


@pytest.mark.asyncio
async def test_delete_group(service):
    response = await service.delete_group(group_id="group_id_example")
    assert response == {'success': 'true'}


@pytest.mark.asyncio
async def test_edit_group(service):
    dto = GroupUpdateDTOFactory()
    response = await service.edit_group(data=dto, group_id="group_id_example")
    assert response is not None


@pytest.mark.asyncio
async def test_disable_group(service):
    dto = GroupStatusUpdateParamsFactory()
    response = await service.disable_group(data=dto, group_id="group_id_example")
    assert response is not None


@pytest.mark.asyncio
async def test_get_calendar_events(service):
    dto: CalendarEventDTO = CalendarEventDTOFactory()
    response = await service.get_calendar_events(dto.startTime, dto.endTime, dto.locationId, dto.calendarId)
    assert response is not None


@pytest.mark.asyncio
async def test_get_blocked_slots(service):
    dto: CalendarEventDTO = CalendarEventDTOFactory()
    response = await service.get_blocked_slots(dto.startTime, dto.endTime, dto.locationId, dto.calendarId)
    assert response is not None


# @pytest.mark.asyncio
# async def test_update_calendar(service):
#     dto = CalendarUpdateDTOFactory()
#     response = await service.update_calendar(data=dto, calendar_id="calendar_id_example")
#     assert response is not None


@pytest.mark.asyncio
async def test_get_calendar(service):
    response = await service.get_calendar(calendar_id="calendar_id_example")
    assert response is not None


@pytest.mark.asyncio
async def test_delete_calendar(service):
    response = await service.delete_calendar(calendar_id="calendar_id_example")
    assert response == {'success': 'true'}


@pytest.mark.asyncio
async def test_get_appointment(service):
    response = await service.get_appointment(event_id="event_id_example")
    assert response is not None


# @pytest.mark.asyncio
# async def test_edit_appointment(service):
#     dto = AppointmentEditSchemaFactory()
#     response = await service.edit_appointment(data=dto, event_id="event_id_example")
#     assert response is not None


# @pytest.mark.asyncio
# async def test_create_appointment(service):
#     dto = AppointmentCreateSchemaFactory()
#     response = await service.create_appointment(data=dto)
#     assert response is not None


@pytest.mark.asyncio
async def test_create_block_slot(service):
    dto = BlockSlotCreateSchemaFactory()
    response = await service.create_block_slot(data=dto)
    assert response is not None


@pytest.mark.asyncio
async def test_edit_block_slot(service):
    dto = BlockSlotEditSchemaFactory()
    response = await service.edit_block_slot(data=dto, event_id="event_id_example")
    assert response is not None


@pytest.mark.asyncio
async def test_delete_event(service):
    dto = DeleteAppointmentSchemaFactory()
    response = await service.delete_event(data=dto, event_id="event_id_example")
    assert response == {'succeeded': True}


@pytest.mark.asyncio
async def test_get_calendar_resource(service):
    response = await service.get_calendar_resource(resource_type="equipments", _id="resource_id_example")
    assert response is None


@pytest.mark.asyncio
async def test_update_calendar_resource(service):
    dto = UpdateCalendarResourceDTOFactory()
    response = await service.update_calendar_resource(data=dto, resource_type="equipments", _id="resource_id_example")
    assert response is None


@pytest.mark.asyncio
async def test_delete_calendar_resource(service):
    response = await service.delete_calendar_resource(resource_type="equipments", _id="resource_id_example")
    assert response is None


@pytest.mark.asyncio
async def test_fetch_calendar_resources(service):
    response = await service.fetch_calendar_resources(resource_type="equipments")
    assert response is not None


@pytest.mark.asyncio
async def test_create_calendar_resource(service):
    dto = CreateCalendarResourceDTOFactory()
    response = await service.create_calendar_resource(data=dto, resource_type="equipments")
    assert response is not None


@pytest.mark.asyncio
async def test_get_calendars(service):
    response = await service.get_calendars()
    assert response is not None


@pytest.mark.asyncio
async def test_create_calendar(service):
    dto = CalendarCreateDTOFactory()
    response = await service.create_calendar(data=dto)
    assert response is not None
