from app.main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncio
import asynctest
import requests
import json


class TestReservation(asynctest.TestCase):
    def create_citizen(self):
        url = "https://wcg-apis.herokuapp.com/registration"
        citizen_id = self.citizen["citizen_id"]
        requests.delete(f"{url}/{citizen_id}")
        res = requests.post(url, params=self.citizen)
        url = "https://wcg-apis.herokuapp.com/reservation"
        site_name = "og"
        requests.delete(f"{url}/{citizen_id}")
        res = requests.post(
            url,
            params={
                "citizen_id": citizen_id,
                "site_name": site_name,
                "vaccine_name": "Astra",
            },
        )

    async def setUp(self) -> None:
        self.queue = asyncio.Queue(maxsize=1)
        self.client = TestClient(app)
        self.base_url = "/api"
        self.site_id = "618235a0ced6e0aec20a422f"
        self.citizen = {
            "citizen_id": "1130594839284",
            "name": "name1",
            "surname": "surname1",
            "birth_date": "11-11-2000",
            "occupation": "student",
            "phone_number": "0194859483",
            "is_risk": "False",
            "address": "bkk",
        }
        self.create_citizen()

    async def test_get_all_reservations(self):
        """Test retrive all the valid reservation."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(
                f"{self.base_url}/site/{self.site_id}/reservations"
            )
            self.assertEqual(200, responses.status_code)

    async def test_get_limit_10_reservations(self):
        """Test retrive limit at 10 valid reservation per page."""
        page = {"limit": 10, "page": 1}
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(
                f"{self.base_url}/site/{self.site_id}/reservations", params=page
            )
            self.assertEqual(200, responses.status_code)
            content = responses.json()["response"]
            self.assertLessEqual(len(content), 10)

    async def test_get_negative_limit_reservations(self):
        """Test retrive using negative limit reservation."""
        page = {
            "limit": -5,
            "page": 1,
        }  # the negative would be convert to 0 automatically
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(
                f"{self.base_url}/site/{self.site_id}/reservations", params=page
            )
            self.assertEqual(200, responses.status_code)
            content = responses.json()["response"]
            self.assertEqual(content["reservations"], [])

    # This may failed if the government module delete the reservation

    async def test_get_reservation(self):
        """Test retrive a specific reservation by giving citizen_id."""
        citizen_id = self.citizen["citizen_id"]
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(
                f"{self.base_url}/site/{self.site_id}/reservation/{citizen_id}"
            )
            self.assertEqual(200, responses.status_code)

    async def test_get_invalid_citizen_reservation(self):
        """Test retrive reservation by giving invalid citizen_id."""
        citizen_id = "11034031341243"
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(
                f"{self.base_url}/site/{self.site_id}/reservation/{citizen_id}"
            )
            self.assertEqual(404, responses.status_code)

    async def test_get_specific_reservation_from_invalid_site_id(self):
        """Test retrive specific reservation by giving invalid service_site id."""
        citizen_id = "1103403134124"
        service_site = "111111111111111111111111"
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(
                f"{self.base_url}/site/{service_site}/reservation/{citizen_id}"
            )
            content = responses.json()
            self.assertEqual(404, responses.status_code)
            self.assertEqual(content["detail"], "site name is not found")

    async def test_get_reservations_from_invalid_site_id(self):
        """Test retrive all reservations by giving invalid service_site id."""
        service_site = "111111111111111111111111"
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(
                f"{self.base_url}/site/{service_site}/reservations"
            )
            self.assertEqual(404, responses.status_code)

    async def test_get_empty_reservation_from_service_site(self):
        """Test retrive reservation from empty service_site."""
        service_site = "6179113760e255455240052b"
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(
                f"{self.base_url}/site/{service_site}/reservations"
            )
            content = responses.json()
            self.assertEqual(
                content["detail"],
                "Reservation in Service site 6179113760e255455240052b not found",
            )
            self.assertEqual(404, responses.status_code)
