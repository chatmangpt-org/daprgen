Feature: Appointment management
  As a user
  I want to manage appointments
  So that I can schedule and organize events

  Scenario: Successfully create a new appointment
    Given I have valid appointment details
    When I create the appointment
    Then the appointment should be created successfully
    And I should be able to retrieve the appointment
    And I should be able to update the appointment
    And I should be able to list all appointments
    And I should be able to delete the appointment
    And the appointment should no longer exist
