# import pytest
# from pytest_bdd import scenarios, given, when, then
#
#
# from daprgen.prototypes.calendar.appointment import Appointment
#
# # from conftest import AppointmentRequestFactory
#
# scenarios('features/appointment.feature')
#
#
# @pytest.fixture
# def appointment_service(repository, event_publisher):
#     return Appointment(repository, event_publisher)
#
#
# @pytest.fixture
# def appointment_request():
#     return AppointmentRequestFactory()
#
#
# @given('I have valid appointment details')
# def valid_appointment_details(appointment_request):
#     return appointment_request
#
#
# @when('I create the appointment')
# async def create_appointment(appointment_service, appointment_request):
#     await appointment_service.create(appointment_request)
#
#
# @then('the appointment should be created successfully')
# async def appointment_created_successfully(appointment_service, appointment_request):
#     appointments = await appointment_service.list()
#     assert any(appt.title == appointment_request.title for appt in appointments)
#
#
# @then('I should be able to retrieve the appointment')
# async def retrieve_appointment(appointment_service, appointment_request):
#     appointments = await appointment_service.list()
#     created_appointment = next(appt for appt in appointments if appt.title == appointment_request.title)
#     retrieved_appointment = await appointment_service.get(created_appointment.id)
#     assert retrieved_appointment.title == appointment_request.title
#
#
# @then('I should be able to update the appointment')
# async def update_appointment(appointment_service, appointment_request):
#     appointments = await appointment_service.list()
#     created_appointment = next(appt for appt in appointments if appt.title == appointment_request.title)
#     appointment_request.title = "Updated Test Event"
#     await appointment_service.update(created_appointment.id, appointment_request)
#     updated_appointment = await appointment_service.get(created_appointment.id)
#     assert updated_appointment.title == "Updated Test Event"
#
#
# @then('I should be able to list all appointments')
# async def list_all_appointments(appointment_service):
#     appointments = await appointment_service.list()
#     assert len(appointments) > 0
#
#
# @then('I should be able to delete the appointment')
# async def delete_appointment(appointment_service, appointment_request):
#     appointments = await appointment_service.list()
#     created_appointment = next(appt for appt in appointments if appt.title == appointment_request.title)
#     await appointment_service.delete(created_appointment.id)
#     appointments = await appointment_service.list()
#     assert all(appt.id != created_appointment.id for appt in appointments)
#
#
# @then('the appointment should no longer exist')
# async def appointment_no_longer_exists(appointment_service, appointment_request):
#     appointments = await appointment_service.list()
#     assert all(appt.title != appointment_request.title for appt in appointments)
