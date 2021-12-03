from ..main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.utils.oauth2 import get_current_user
import requests_mock
import asynctest


def override_get_current_user():
    valid_user = {"username": "Tester", "password": "tester123"}
    return valid_user


app.dependency_overrides[get_current_user] = override_get_current_user


class TestServiceSite(asynctest.TestCase):
    async def setUp(self) -> None:
        self.client = TestClient(app)
        self.base_url = "/api"
        self.auth_url = "/login"
        self.valid_user = {"username": "Tester", "password": "tester123"}
        self.valid_service_site = {
            "name": "สถานีกลางบางซื่อ",
            "location": {
                "formatted_address": "336 ซอยกำแพงเพชร 2 ถนนเทอดดำริ แขวงจตุจักร เขตจตุจักร กรุงเทพมหานคร",
                "country": "ไทย",
                "postal": "10900",
                "route": "เทอดดำริ",
                "city": "กรุงเทพมหานคร",
                "coordinates": {"latitude": 13.80375, "longitude": 100.54225},
            },
            "capacity": 20000,
        }
        self.valid_site_id = "61a675cdcdfc0e87ab74b90d"

    async def test_get_all_service_site(self):
        """Test retrive all the valid service sites."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(f"{self.base_url}/sites")
            self.assertEqual(200, responses.status_code)

    async def test_get_service_site(self):
        """Test retrive specific service sites using its id which is 24 characters."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(f"{self.base_url}/site/{self.valid_site_id}")
            self.assertEqual(200, responses.status_code)

    async def test_get_invalid_service_site(self):
        """Test retrive invalid service sites."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(f"{self.base_url}/site/619f7c3289c2942b7d28f5e0")
            self.assertEqual(404, responses.status_code)

    async def test_insert_service_site(self):
        """Test inserted service site with corrected format using mock request_mock."""
        valid_service_site = {
            "name": "เซ็นทรัลพลาซา เวสเกต",
            "location": {
                "formatted_address": "หมู่ที่ 6 199/1-2 ถ. กาญจนาภิเษก ตำบล เสาธงหิน อำเภอบางใหญ่ นนทบุรี 11140",
                "country": "ไทย",
                "postal": "11140",
                "route": "กาญจนาภิเษก",
                "city": "นนทบุรี ",
                "coordinates": {"latitude": 13.87719, "longitude": 100.41136},
            },
            "capacity": 5000,
        }
        with requests_mock.Mocker() as rm:
            rm.post(f"{self.base_url}/site", json=valid_service_site)
            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.post(
                    f"{self.base_url}/site", json=valid_service_site
                )
                self.assertEqual(201, response.status_code)

    async def test_insert_service_site_with_invalid_data(self):
        """Test inserted service site with corrected format using mock request_mock."""
        valid_service_site = self.valid_service_site
        valid_service_site.pop("location")
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(f"{self.base_url}/site", json=valid_service_site)
            self.assertEqual(422, response.status_code)

    async def test_update_service_site(self):
        """Test updated valid service site using mock request_mock."""
        updated_value = self.valid_service_site
        updated_value.update({"name": "OGYH"})
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.put(
                f"{self.base_url}/site/{self.valid_site_id}", json=updated_value
            )
            self.assertEqual(200, responses.status_code)
            responses = await ac.get(f"{self.base_url}/site/{self.valid_site_id}")
            content = responses.json()
            del content["id"]  # we don't object id at first
            self.assertEqual(self.valid_service_site, content)

    async def test_update_invalid_service_site(self):
        """Test updated invalid service site using mock request_mock."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.put(
                f"{self.base_url}/site/619f7c3289c2942b7d28f5e1",
                json=self.valid_service_site,
            )
            self.assertEqual(404, responses.status_code)

    async def test_remove_service_site(self):
        """Test remove valid service site using its id which is 24 characters."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            with requests_mock.Mocker() as rm:
                rm.post(f"{self.base_url}/site", json=self.valid_service_site)
                rm.delete(f"{self.base_url}/site/{self.valid_site_id}")

    async def test_remove_invalid_12_byte_hex_service_site_id(self):
        """Test remove invalid service site using its id which is 24 characters."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.delete(
                f"{self.base_url}/site/619f7c3289c2942b7d28f5e0"
            )
            self.assertEqual(404, responses.status_code)

    async def test_remove_invalid_service_site(self):
        """Test remove valid service site using 1 character as its id."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(f"{self.base_url}/site/1")
            self.assertEqual(404, response.status_code)
