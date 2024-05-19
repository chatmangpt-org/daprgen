import requests
import json

# Define the URL and headers
url = "https://stoplight.io/mocks/highlevel/integrations/39582850"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer sdfdsf",
    "Content-Type": "application/json",
    "Version": "2021-04-15"
}

# Define the data payload
calendar_data = {
    "notifications": [
        {
            "type": "email",
            "shouldSendToContact": True,
            "shouldSendToGuest": True,
            "shouldSendToUser": True,
            "shouldSendToSelectedUsers": True,
            "selectedUsers": "user1@testemail.com,user2@testemail.com"
        }
    ],
    "locationId": "ocQHyuzHvysMo5N5VsXc",
    "groupId": "BqTwX8QFwXzpegMve9EQ",
    "teamMembers": [
        {
            "userId": "ocQHyuzHvysMo5N5VsXc",
            "priority": 0.5,
            "meetingLocationType": "custom",
            "meetingLocation": "string",
            "isPrimary": True
        }
    ],
    "eventType": "RoundRobin_OptimizeForAvailability",
    "name": "test calendar",
    "description": "this is used for testing",
    "slug": "test1",
    "widgetSlug": "test1",
    "workspaceSlug": "test1",
    "serviceNodeId": "string",
    "prismUrl": "https://prism-url.com",
    "calendarType": "round_robin",
    "widgetType": "classic",
    "eventTitle": "{{contact.name}}",
    "eventColor": "#039be5",
    "meetingLocation": "string",
    "slotDuration": 30,
    "preBufferUnit": "mins",
    "slotInterval": 30,
    "slotBuffer": 0,
    "preBuffer": 0,
    "appoinmentPerSlot": 1,
    "appoinmentPerDay": 0,
    "openHours": [
        {
            "daysOfTheWeek": [0],
            "hours": [
                {
                    "openHour": 0,
                    "openMinute": 0,
                    "closeHour": 0,
                    "closeMinute": 0
                }
            ]
        }
    ],
    "enableRecurring": True,
    "recurring": {},
    "formId": "string",
    "stickyContact": True,
    "isLivePaymentMode": True,
    "autoConfirm": True,
    "shouldSendAlertEmailsToAssignedMember": True,
    "alertEmail": "string",
    "googleInvitationEmails": False,
    "allowReschedule": True,
    "allowCancellation": True,
    "shouldAssignContactToTeamMember": True,
    "shouldSkipAssigningContactForExisting": True,
    "notes": "string",
    "pixelId": "string",
    "formSubmitType": "ThankYouMessage",
    "formSubmitRedirectURL": "string",
    "formSubmitThanksMessage": "string",
    "availabilityType": 0,
    "availabilities": [
        {
            "id": "string",
            "date": "2023-09-24T00:00:00.000Z",
            "hours": [
                {
                    "openHour": 0,
                    "openMinute": 0,
                    "closeHour": 0,
                    "closeMinute": 0
                }
            ],
            "deleted": False
        }
    ],
    "guestType": "count_only",
    "consentLabel": "string",
    "calendarCoverImage": "https://path-to-image.com",
    "id": "0TkCdp9PfvLeWKYRRvIz",
}



def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    # Send the PUT request
    response = requests.put(url, headers=headers, data=json.dumps(calendar_data))

    # Print the response
    print(response.status_code)
    print(response.json())


if __name__ == '__main__':
    main()
