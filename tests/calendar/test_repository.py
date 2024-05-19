import pytest
from httpx import AsyncClient, Request, Response
from uuid import uuid4
from daprgen.prototypes.calendar.models import AppointmentResponse
from daprgen.prototypes.calendar.repository import GoHighLevelAppointmentRepository


@pytest.fixture
def mock_response(mocker):
    return mocker.patch("httpx.AsyncClient")


@pytest.fixture
def repository():
    return GoHighLevelAppointmentRepository()


@pytest.fixture
def sample_appointment_response():
    return AppointmentResponse(
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


@pytest.mark.asyncio
async def test_create_appointment(repository, sample_appointment_response, mock_response):
    mock_response.return_value.post.return_value = Response(
        status_code=201,
        request=Request('POST', repository.BASE_URL),
        json=sample_appointment_response.model_dump_json()
    )

    await repository.create(sample_appointment_response)
    mock_response.return_value.post.assert_called_once_with(
        repository.BASE_URL,
        headers=repository.HEADERS,
        json=sample_appointment_response.model_dump_json()
    )


@pytest.mark.asyncio
async def test_get_appointment(repository, sample_appointment_response, mock_response):
    mock_response.return_value.get.return_value = Response(
        status_code=200,
        request=Request('GET', f"{repository.BASE_URL}/{sample_appointment_response.id}"),
        json=sample_appointment_response.model_dump_json()
    )

    result = await repository.get(sample_appointment_response.id)
    assert result == sample_appointment_response
    mock_response.return_value.get.assert_called_once_with(
        f"{repository.BASE_URL}/{sample_appointment_response.id}",
        headers=repository.HEADERS
    )


@pytest.mark.asyncio
async def test_update_appointment(repository, sample_appointment_response, mock_response):
    mock_response.return_value.put.return_value = Response(
        status_code=200,
        request=Request('PUT', f"{repository.BASE_URL}/{sample_appointment_response.id}"),
        json=sample_appointment_response.model_dump_json()
    )

    await repository.update(sample_appointment_response.id, sample_appointment_response)
    mock_response.return_value.put.assert_called_once_with(
        f"{repository.BASE_URL}/{sample_appointment_response.id}",
        headers=repository.HEADERS,
        json=sample_appointment_response.model_dump_json()
    )


@pytest.mark.asyncio
async def test_delete_appointment(repository, sample_appointment_response, mock_response):
    mock_response.return_value.delete.return_value = Response(
        status_code=204,
        request=Request('DELETE', f"{repository.BASE_URL}/{sample_appointment_response.id}")
    )

    await repository.delete(sample_appointment_response.id)
    mock_response.return_value.delete.assert_called_once_with(
        f"{repository.BASE_URL}/{sample_appointment_response.id}",
        headers=repository.HEADERS
    )


@pytest.mark.asyncio
async def test_list_appointments(repository, sample_appointment_response, mock_response):
    mock_response.return_value.get.return_value = Response(
        status_code=200,
        request=Request('GET', repository.BASE_URL),
        json=[sample_appointment_response.model_dump_json()]
    )

    result = await repository.list()
    assert len(result) == 1
    assert result[0] == sample_appointment_response
    mock_response.return_value.get.assert_called_once_with(
        repository.BASE_URL,
        headers=repository.HEADERS
    )
