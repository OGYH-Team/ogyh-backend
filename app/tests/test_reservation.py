from starlette import responses
from app.main import app
from fastapi.testclient import TestClient
import unittest

class TestReservation(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(app)
        self.base_url = "/api"
        self.site_id = "618235a0ced6e0aec20a422f"

    def test_get_all_reservations(self):
        """Test retrive all the valid reservation."""
        responses = self.client.get(f"{self.base_url}/site/{self.site_id}/reservations")
        self.assertEqual(200, responses.status_code)

    def test_get_10_reservations(self):
        """Test retrive all the valid reservation."""
        page = {"limit": 10, "page": 1}
        responses = self.client.get(f"{self.base_url}/site/{self.site_id}/reservations", params=page)
        self.assertEqual(200, responses.status_code)
        content = responses.json()["response"]
        self.assertLessEqual(len(content), 10)

    def test_get_reservation(self):
        """Test retrive a specific reservation by given citizen_id."""
        citizen_id = "1103403134124"
        responses = self.client.get(f"{self.base_url}/site/{self.site_id}/reservation/{citizen_id}")
        self.assertEqual(200, responses.status_code)

    def test_get_reservation_invalid(self):
        """Test retrive invalid reservation."""
        citizen_id = "11034031341243"
        responses = self.client.get(f"{self.base_url}/site/{self.site_id}/reservation/{citizen_id}")
        self.assertEqual(404, responses.status_code)    