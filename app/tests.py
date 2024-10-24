from django.test import TestCase, Client
from django.urls import reverse
import json

class TrainNamesAPITest(TestCase):
    def setUp(self):
        # Setup run before every test.
        self.client = Client()

        # Sample data for testing
        self.valid_payload = {
                "from_station_name": "Dhaka",
                "to_station_name": "Khulna",
                "date": "2024-10-25"
                }

    def test_get_train_names_success(self):
        # Test successful POST request
        response = self.client.post(
                reverse('get_train_names'),
                data=json.dumps(self.valid_payload),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 200)  # Ensure the response is OK
        self.assertIsInstance(response.json(), list)  # Ensure the response is a list

    def test_get_train_names_invalid_date(self):
        # Test with invalid date format
        invalid_payload = {
                "from_station_name": "Dhaka",
                "to_station_name": "Khulna",
                "date": "invalid-date"
                }
        response = self.client.post(
                reverse('get_train_names'),
                data=json.dumps(invalid_payload),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 400)  # Ensure the response is a Bad Request
        self.assertIn("error", response.json())  # Ensure the error is returned in the response

