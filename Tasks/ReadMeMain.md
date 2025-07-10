# API Test Suite

A comprehensive test suite for validating API endpoints with automated discovery and execution.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Run all tests:**
   ```bash
   python run_all_tests.py
   ```

3. **Run with verbose output:**
   ```bash
   python run_all_tests.py --verbose
   ```

## 📁 Project Structure

```

├── run_all_tests.py           # Main test runner (run this!)
├── README.md                  # This file
├── QA_Get_Task_WithContact.py # Tasks API contactId tests
└── README.md                  # Tasks API test documentation
```

## 🔧 Test Runner Features

### Automatic Test Discovery
The main runner automatically finds and runs:
- Files matching `*test*.py` pattern
- Files starting with `QA_*.py` (quality assurance tests)
- All Python test files in subdirectories

### Unified Execution
- Single command runs all tests
- Consistent output format
- Comprehensive summary report
- Exit codes for CI/CD integration

### Example Output
```
🔍 Discovering test files...
📁 Found 1 test file(s):
  - QA_Get_Task_WithContact.py

🚀 Running all tests...

============================================================
RUNNING: QA_Get_Task_WithContact.py
============================================================
Testing endpoint: https://sandbox-salesforce-data-api.us-e2.cloudhub.io/api/tasks
Using Contact ID: 003cX00000L4qIlQAJ

test_01_missing_contact_id_returns_400 ... ok
test_02_empty_contact_id_returns_200_with_empty_list ... ok
test_03_invalid_contact_id_returns_400_or_404 ... ok
test_04_valid_contact_id_returns_200_with_tasks ... ok

============================================================
📊 TEST SUMMARY
============================================================
Files run: 1
Files passed: 1
Files failed: 0
Total tests: 4
Total failures: 0
Total errors: 0

✅ ALL TESTS PASSED!

Detailed results:
  ✅ PASS QA_Get_Task_WithContact.py (4 tests, 0 failures, 0 errors)
```

## 📋 Current Test Suites

### 1. Tasks API contactId Tests (`QA_Get_Task_WithContact.py`)
Tests the `/api/tasks` endpoint's `contactId` parameter handling.

**Test Cases:**
- Missing `contactId` parameter → `400 Bad Request`
- Empty `contactId` value → `200 OK` with empty array
- Invalid `contactId` formats → `400/404` error
- Valid `contactId` → `200 OK` with task data

**Configuration Required:**
```python
cls.base_url = "https://your-api-url.com/api"
cls.valid_contact_id = "003cX00000L4qIlQAJ"  # Replace with real Contact ID
```

## 🔧 Adding New Tests

### Method 1: Create a new test file
1. Create a new Python file (e.g., `QA_New_Feature.py` or `test_new_feature.py`)
2. Follow the unittest framework pattern
3. The main runner will automatically discover and run it

### Method 2: Extend existing test files
1. Add new test methods to existing test classes
2. Follow the naming convention: `test_XX_descriptive_name`

### Test File Template
```python
import unittest
import requests
import json

class NewFeatureTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.base_url = "https://your-api-url.com/api"
        cls.endpoint = f"{cls.base_url}/your-endpoint"
        cls.headers = {
            "Content-Type": "application/json"
        }
    
    def test_01_your_test_case(self):
        """Test description"""
        # Your test code here
        pass
    
    def test_02_another_test_case(self):
        """Another test description"""
        # Your test code here
        pass

if __name__ == '__main__':
    unittest.main()
```

## 🔍 Configuration Guide

### Authentication Setup
Most tests require authentication. Configure in each test file's `setUpClass()`:

```python
cls.headers = {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "Content-Type": "application/json",
    "Authorization": "Bearer your_token"  # if needed
}
```

### Environment-Specific Configuration
Consider using environment variables for sensitive data:

```python
import os

cls.base_url = os.getenv('API_BASE_URL', 'https://default-url.com/api')
cls.client_id = os.getenv('API_CLIENT_ID', 'default_client_id')
cls.client_secret = os.getenv('API_CLIENT_SECRET', 'default_secret')
```

### Test Data Management
For tests requiring specific data:

```python
# Use real IDs from your system
cls.valid_contact_id = "003cX00000L4qIlQAJ"
cls.valid_account_id = "001cX00000L4qIlQAJ"

# Define expected response structures
cls.expected_task_fields = ['Id', 'Subject', 'Due_Date__c', 'Status']
```

## 🚨 Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify `base_url` is correct
   - Check network connectivity
   - Confirm API endpoint is accessible

2. **Authentication Failures**
   - Verify client credentials
   - Check token expiration
   - Ensure proper header format

3. **Test Data Issues**
   - Use real IDs from your system
   - Verify data exists in the target environment
   - Check field names match API response

4. **Import Errors**
   - Ensure all required packages are installed
   - Check Python path configuration
   - Verify file permissions

### Debug Mode
Run individual test files directly for detailed debugging:
```bash
python QA_Get_Task_WithContact.py
```

### Manual API Testing
Test your API manually to verify expected behavior:
```bash
curl -X GET "https://your-api-url.com/api/tasks?contactId=003cX00000L4qIlQAJ" \
  -H "client_id: your_client_id" \
  -H "client_secret: your_client_secret"
```

## 🎯 Best Practices

### Test Organization
- Use descriptive test method names
- Group related tests in the same file
- Add clear docstrings for each test
- Use `self.subTest()` for testing multiple similar scenarios

### Assertion Patterns
```python
# Status code assertions
self.assertEqual(response.status_code, 200)

# JSON response assertions
response_data = response.json()
self.assertIsInstance(response_data, list)
self.assertGreater(len(response_data), 0)

# Field validation
self.assertIn('Id', task)
self.assertIsNotNone(task['Id'])
```

### Error Handling
```python
try:
    response_data = response.json()
except json.JSONDecodeError:
    self.fail(f"Expected JSON response, got: {response.text}")
```

## 📊 Continuous Integration

### Exit Codes
- `0`: All tests passed
- `1`: One or more tests failed

### CI/CD Integration
```yaml
# Example GitHub Actions workflow
- name: Run API Tests
  run: |
    pip install requests
    python run_all_tests.py
```

### Reporting
The test runner provides structured output suitable for:
- Console monitoring
- CI/CD pipeline integration
- Automated reporting systems

## 🔄 Future Enhancements

### Planned Features
- [ ] HTML test report generation
- [ ] Test configuration file support
- [ ] Parallel test execution
- [ ] Test result persistence
- [ ] Performance testing capabilities
- [ ] Mock server integration
- [ ] Test data fixture management

### Contributing
When adding new tests:
1. Follow the existing naming conventions
2. Include comprehensive documentation
3. Add appropriate error handling
4. Test both success and failure scenarios
5. Update this README with new test descriptions

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review individual test README files
3. Verify your API configuration
4. Test endpoints manually before running automated tests

---

**Happy Testing! 🧪**