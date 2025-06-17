Tasks API contactId Endpoint Test Suite
This test suite is designed to validate the /api/tasks endpoint, which accepts a contactId parameter, ensuring it adheres to expected behavior for various input scenarios.

🚀 Getting Started
1. Install Requirements
Ensure you have the requests library installed:

Bash

pip install requests

2. Configure the Test Suite
Open your test file (test_tasks_api.py or similar) and update the following values within the setUpClass() method:

Python

# Your API base URL
cls.base_url = "https://sandbox-salesforce-data-api.us-e2.cloudhub.io/api" # Example provided

# A valid Contact ID that exists in your system and ideally has associated tasks
cls.valid_contact_id = "003cXxxxxxxxxxxx" # REPLACE WITH YOUR ACTUAL VALID CONTACT ID

# Field names your API returns for a task object (verify with a manual API call first)
cls.expected_task_fields = ['Id', 'Subject', 'Due_Date__c', 'Status', 'Contact__c']
3. Run the Tests
Execute the tests from your terminal:

Bash

python your_test_file_name.py
✅ Pre-Test Checklist
Before running the tests, please verify the following:

[ ] API Endpoint Accessibility: The cls.base_url is correct and the API endpoint is reachable.
[ ] Valid Contact ID: You have a genuine contactId that exists in the Salesforce environment your API connects to.
[ ] Associated Tasks: The chosen contactId preferably has some tasks linked to it to fully validate successful responses.
[ ] API Field Names: You've confirmed the exact field names (e.g., Due_Date__c vs. DueDate) returned by your API.
[ ] Network Connectivity: Your machine has a stable internet connection.
🔍 How to Find Your Contact ID
Here are a few ways to obtain a ContactId for testing:

Method 1: From Salesforce UI
Log into your Salesforce instance.
Navigate to any Contact record.
Copy the 18-character ID from the URL in your browser's address bar. It typically starts with 003.
Method 2: Manual API Test (if you have other ways to query Salesforce data)
You can try a generic ID or an ID you expect to be valid to see the response structure:

Bash

curl "http://your-api-url.com/api/tasks?contactId=003000000000000"
Method 3: Salesforce SOQL Query (using a tool like Workbench or Developer Console)
SQL

SELECT Id, Name FROM Contact LIMIT 1

📊 Essential Test Cases
This suite includes 4 critical tests to ensure the robustness of your /api/tasks endpoint.

Test #	Test Name	Purpose	Expected Result
1	Missing contactId	Validates required parameter enforcement	400 Bad Request
2	Empty contactId	Validates handling of empty string input	200 OK with an empty list ([])
3	Invalid contactId format	Validates input ID format	400 Bad Request or 404 Not Found
4	Valid contactId	Validates successful data retrieval	200 OK with a list of task objects

Export to Sheets
🎯 Expected Test Results
🎉 Perfect Success (All 4 Pass)
Testing endpoint: https://sandbox-salesforce-data-api.us-e2.cloudhub.io/api/tasks
Using Contact ID: 003cX00000L4qIlQAJ
test_01_missing_contact_id_returns_400 (__main__.TasksContactIdTests) ... Request: {} -> Status: 400
  Expected 400 Bad Request for missing contactId.
  Response Body: {
    "error": "Missing required parameter: contactId"
  }
ok
test_02_empty_contact_id_returns_200_with_empty_list (__main__.TasksContactIdTests) ... Request: {'contactId': ''} -> Status: 200
  Expected 200 OK with an empty list for empty contactId.
  Response Body: []
ok
test_03_invalid_contact_id_returns_400_or_404 (__main__.TasksContactIdTests) ... Request: {'contactId': 'INVALID'} -> Status: 400
  Expected 400 or 404 for invalid contactId 'INVALID'.
  Response Body: {
    "error": "Invalid contactId format"
  }
Request: {'contactId': '123'} -> Status: 400
  Expected 400 or 404 for invalid contactId '123'.
  Response Body: {
    "error": "Invalid contactId format"
  }
Request: {'contactId': 'abc123'} -> Status: 400
  Expected 400 or 404 for invalid contactId 'abc123'.
  Response Body: {
    "error": "Invalid contactId format"
  }
Request: {'contactId': '003INVALID'} -> Status: 400
  Expected 400 or 404 for invalid contactId '003INVALID'.
  Response Body: {
    "error": "Invalid contactId format"
  }
ok
test_04_valid_contact_id_returns_200_with_tasks (__main__.TasksContactIdTests) ... Request: {'contactId': '003cX00000L4qIlQAJ'} -> Status: 200
  Expected 200 OK for valid contactId '003cX00000L4qIlQAJ'.
  Response Body (2 tasks): [
    {
      "Id": "00Txxxxxxxxxxxxxxx",
      "Subject": "Follow up with John Doe",
      "Due_Date__c": "2025-07-01",
      "Status": "Open",
      "Contact__c": "003cX00000L4qIlQAJ"
    },
    {
      "Id": "00Tyyyyyyyyyyyyyyy",
      "Subject": "Schedule meeting with Jane Smith",
      "Due_Date__c": "2025-06-25",
      "Status": "In Progress",
      "Contact__c": "003cX00000L4qIlQAJ"
    }
  ]
Found 2 tasks for contact 003cX00000L4qIlQAJ
ok

----------------------------------------------------------------------
Ran 4 tests in X.XXXs

OK

🚫 Common Failure Scenarios
If a test fails, the output will provide a traceback and an assertion error message. Here are some common reasons and their fixes:

Scenario 1: Wrong contactId
FAILED test_04_valid_contact_id_returns_200_with_tasks
AssertionError: 400 != 200 : Valid contactId should return 200 OK
Fix: Update cls.valid_contact_id in setUpClass() with a real, existing Contact ID from your system. Check the DEBUG INFO output if you have it enabled for test_04 for the API's error message.

Scenario 2: Incorrect Field Names in expected_task_fields
FAILED test_04_valid_contact_id_returns_200_with_tasks
AssertionError: Task missing required field: Due_Date__c
Fix: Update cls.expected_task_fields in setUpClass() to exactly match the field names your API returns in its JSON response (e.g., Due_Date__c vs dueDate).

Scenario 3: Wrong API URL or Connectivity Issues
ERROR test_01_missing_contact_id_returns_400
requests.exceptions.ConnectionError: ...
Fix: Update cls.base_url in setUpClass() with your correct API endpoint. Ensure network connectivity to the API.

🛠 Quick Troubleshooting
Issue: All tests fail with connection errors
Action: Manually test your API endpoint using curl or Postman to confirm it's accessible and responding.
Bash

curl "http://your-api-url.com/api/tasks?contactId=test"
Issue: Test 4 fails - wrong field names or unexpected response structure
Action: Perform a manual API call with a known valid contactId and inspect the exact JSON response structure.
Bash

curl "http://your-api-url.com/api/tasks?contactId=YOUR_VALID_CONTACT_ID" | python -m json.tool
(Replace YOUR_VALID_CONTACT_ID with an actual ID).
Issue: Need Authentication/Authorization
If your API requires authentication (e.g., API keys, OAuth tokens), you'll need to add them to the headers dictionary in setUpClass(). For example:

Python

cls.headers = {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_ACTUAL_ACCESS_TOKEN" # Add if your API uses Bearer tokens
}
💡 Customization Options
This test suite is flexible and can be extended for more specific needs.

Change API Response Time Limit (if adding a performance test)
If you decide to add a performance test (e.g., test_05_response_time), you can modify the assertion for response time:

Python

# Example for a hypothetical test_05
# self.assertLess(response.elapsed.total_seconds(), 5.0, "Response time exceeded 5 seconds")
# Change '5.0' to your desired limit in seconds.
Add Custom Field Validation
Beyond checking for the presence of fields, you can add more specific data validation within validate_task_structure():

Python

def validate_task_structure(self, task: Dict[str, Any]) -> None:
    # Original validation for required fields
    for field in self.expected_task_fields:
        self.assertIn(field, task, f"Task missing required field: {field}")

    # Add your custom validations here:
    if 'Status' in task:
        valid_statuses = ['Open', 'Completed', 'In Progress', 'Deferred']
        self.assertIn(task['Status'], valid_statuses, f"Invalid Status value: '{task['Status']}'")

    if 'Due_Date__c' in task and task['Due_Date__c'] is not None:
        try:
            # Example: Ensure Due_Date__c is a valid date string (YYYY-MM-DD)
            datetime.strptime(task['Due_Date__c'], '%Y-%m-%d')
        except ValueError:
            self.fail(f"Invalid Due_Date__c format for task {task.get('Id')}: {task['Due_Date__c']}")
Test Different Contact IDs
You can extend setUpClass() to define multiple contact IDs and loop through them in your test_04_valid_contact_id_returns_200_with_tasks or dedicated tests:

Python

# In setUpClass(), add multiple test IDs:
cls.test_contact_ids = [
    "003XXXXXXXXXXXXXXXXX",  # Contact with tasks
    "003YYYYYYYYYYYYYYYYY",  # Contact without tasks
    "003ZZZZZZZZZZZZZZZZZ",  # Another contact
]

# Then modify test_04 (or a new test) to loop through all IDs:
# for contact_id in self.test_contact_ids:
#    with self.subTest(contactId=contact_id):
#        params = {'contactId': contact_id}
#        response = self.make_request(params)
#        # ... continue with assertions for each ID