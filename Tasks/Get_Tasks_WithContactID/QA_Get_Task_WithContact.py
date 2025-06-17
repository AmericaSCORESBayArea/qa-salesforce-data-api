import unittest
import requests
import json
from datetime import datetime
from typing import Dict, Any

class TasksContactIdTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test configuration - UPDATE THESE VALUES BEFORE RUNNING"""
        cls.base_url = "https://sandbox-salesforce-data-api.us-e2.cloudhub.io/api"
        cls.endpoint = f"{cls.base_url}/tasks"

        # *** UPDATE THIS VALUE WITH YOUR ACTUAL TEST DATA ***
        cls.valid_contact_id = "003cX00000L4qIlQAJ"  # Replace with valid Contact ID

        # Expected response structure - UPDATE BASED ON YOUR API
        cls.expected_task_fields = ['Id', 'Subject', 'Due_Date__c', 'Status', 'Contact__c']

        # Add headers here
        cls.headers = {
            "client_id": "6a0d25464c774820b5471a8e2290f62c",
            "client_secret": "0155E391d7a84740B223aB693602D3C0",
            "Content-Type": "application/json"
            # Add any other headers as needed
        }

        print(f"Testing endpoint: {cls.endpoint}")
        print(f"Using Contact ID: {cls.valid_contact_id}")

    def make_request(self, params: Dict[str, Any]) -> requests.Response:
        """Helper method to make GET requests to the tasks endpoint"""
        try:
            response = requests.get(self.endpoint, params=params, headers=self.headers, timeout=30)
            print(f"Request: {params} -> Status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            self.fail(f"Request failed: {e}")

    def validate_task_structure(self, task: Dict[str, Any]) -> None:
        """Helper method to validate task object structure"""
        for field in self.expected_task_fields:
            self.assertIn(field, task, f"Task missing required field: {field}")


    def test_01_missing_contact_id_returns_400(self):
        """Test 1: Missing contactId parameter should return 400 Bad Request"""
        params = {}
        response = self.make_request(params)

        print(response.status_code)

        # --- Added for Postman-like output of error response ---
        print(f"  Expected 400 Bad Request for missing contactId.")
        try:
            response_data = response.json()
            print(f"  Response Body: {json.dumps(response_data, indent=2)}")
            error_message = str(response_data).lower()
            self.assertTrue('contactid' in error_message or 'contact' in error_message,
                            "Error message should mention contactId requirement")
        except json.JSONDecodeError:
            print(f"  Response Body (non-JSON): {response.text}")
            self.fail(f"Expected JSON error response, got: {response.text}")
        except Exception as e:
            print(f"  Error parsing response JSON: {e}")
            pass
        # --- End added section ---

    def test_02_empty_contact_id_returns_200_with_empty_list(self): # Renamed for clarity
        """Test 2: Empty contactId parameter should return 200 OK with an empty list"""
        params = {'contactId': ''}
        response = self.make_request(params)

        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200,
                         "Empty contactId should return 200 OK")

        # Assert that the response is a JSON list
        response_data = response.json()
        self.assertIsInstance(response_data, list,
                              "Response for empty contactId should be a list")

        # Assert that the list is empty (as no tasks should be found for an empty contactId)
        self.assertEqual(len(response_data), 0,
                         "Response list for empty contactId should be empty")

        # --- Added for Postman-like output of successful response ---
        print(f"  Expected 200 OK with an empty list for empty contactId.")
        print(f"  Response Body: {json.dumps(response_data, indent=2)}")
        # --- End added section ---



    def test_03_invalid_contact_id_returns_400_or_404(self):
        """Test 3: Invalid contactId format should return 400 or 404"""
        invalid_ids = ['INVALID', '123', 'abc123', '003INVALID']
        
        for invalid_id in invalid_ids:
            with self.subTest(contactId=invalid_id):
                params = {'contactId': invalid_id}
                response = self.make_request(params)
                print(response.status_code)
                # --- Added for Postman-like output of error response ---
                print(f"  Expected 400 or 404 for invalid contactId '{invalid_id}'.")
                try:
                    response_data = response.json()
                    print(f"  Response Body: {json.dumps(response_data, indent=2)}")
                except json.JSONDecodeError:
                    print(f"  Response Body (non-JSON): {response.text}")
                # --- End added section ---

                

    def test_04_valid_contact_id_returns_200_with_tasks(self):
        """Test 4: Valid contactId should return 200 OK with properly structured tasks"""
        params = {'contactId': self.valid_contact_id}
        response = self.make_request(params)

        # --- Debugging code retained for detailed output if failure occurs ---
        if response.status_code != 200:
            print(f"\n--- DEBUG INFO for test_04 (Valid Contact ID Request) ---")
            print(f"URL: {response.url}")
            print(f"Request Headers: {self.headers}")
            print(f"Request Params: {params}")
            print(f"Actual Status Code: {response.status_code}")
            try:
                print(f"Response JSON Body: {response.json()}")
            except json.JSONDecodeError:
                print(f"Response Text Body: {response.text}")
            print(f"---------------------------------------------------\n")
        # --- End debugging code ---
        
        # Response should be JSON list
        response_data = response.json()
    

        # --- Added for Postman-like output of successful response ---
        print(f"  Expected 200 OK for valid contactId '{self.valid_contact_id}'.")
        print(f"  Response Body ({len(response_data)} tasks): {json.dumps(response_data, indent=2)}")
        # --- End added section ---

        

def run_essential_tests():
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TasksContactIdTests)

    # Run tests with detailed output
    # buffer=True hides stdout/stderr unless the test fails, which we don't want here
    # to see the print statements. Set buffer=False or remove it.
    runner = unittest.TextTestRunner(verbosity=2, buffer=False)
    result = runner.run(suite)
    return result.wasSuccessful() # Return whether all tests passed


if __name__ == '__main__':
    success = run_essential_tests()
    if success:
        print("\nAll essential tests passed!")
    else:
        print("\nSome essential tests failed. Check the logs above.")