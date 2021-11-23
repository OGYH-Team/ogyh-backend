from unittest.case import skip
from ..main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.utils.oauth2 import get_current_user
import bson
import requests_mock
import json
import asynctest

def override_get_current_user():
    valid_user = {
            "username": "Tester",
            "password": "tester123"
    }
    return valid_user

app.dependency_overrides[get_current_user] = override_get_current_user

class TestServiceSite(asynctest.TestCase):
    async def setUp(self) -> None:
        self.client = TestClient(app)
        self.base_url = "/api"
        self.auth_url = "/login"
        self.valid_user = {
            "username": "Tester",
            "password": "tester123"
        }

    async def test_get_all_service_site(self):
        """Test retrive all the valid service sites."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(f"{self.base_url}/sites")
        self.assertEqual(200, responses.status_code)

    async def test_get_service_site(self):
        """Test retrive specific service sites using its id which is 24 characters."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(f"{self.base_url}/site/617923857ad4eeefea76d121")
        self.assertEqual(200, responses.status_code)

    async def test_get_invalid_service_site(self):
        """Test retrive invalid service sites."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(f"{self.base_url}/site/617923857ad4eeefea76d120")
        self.assertEqual(404, responses.status_code)

    @skip("Not sure, will be fixed in the future")
    def test_insert_service_site(self):
        """Test inserted service site with corrected format using mock request_mock."""
        data = {"name": "ogyh2", "location": "12345"}
        with requests_mock.Mocker() as rm:
            rm.post(f"{self.base_url}/site", json=data)
            response = self.client.post(f"{self.base_url}/site", params=data)
        self.assertEqual(201, response.status_code)

    async def test_insert_service_site_with_invalid_data(self):
        """Test inserted service site with corrected format using mock request_mock."""
        data = {"hello": "ogyh2", "location": "12345"}
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await ac.post(f"{self.auth_url}", data=self.valid_user)
            response = await ac.post(f"{self.base_url}/site", params=data)
        self.assertEqual(422, response.status_code)

    async def test_update_service_site(self):
        """Test updated valid service site using mock request_mock."""
        data = {"name": "OGYH2", "location": "bangkok"}
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.put(
                f"{self.base_url}/site/617923857ad4eeefea76d121", data=json.dumps(data)
            )
            self.assertEqual(200, responses.status_code)
            responses = await ac.get(f"{self.base_url}/site/617923857ad4eeefea76d121")
            self.assertEqual(
                {"name": "OGYH2", "location": "bangkok"}, responses.json()["response"]
            )

    async def test_update_invalid_service_site(self):
        """Test updated invalid service site using mock request_mock."""
        data = {"name": "OGYH2", "location": "bangkok"}
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.put(
                f"{self.base_url}/site/617923857ad4eeefea76d120", data=json.dumps(data)
            )
            self.assertEqual(404, responses.status_code)

    async def test_remove_service_site(self):
        """Test remove valid service site using its id which is 24 characters."""
        data = {"name": "ogyh666", "location": "12345"}
        async with AsyncClient(app=app, base_url="http://test") as ac:
            with requests_mock.Mocker() as rm:
                rm.post(f"{self.base_url}/site", json=data)
                rm.delete(
                    f"https://ogyh-backend-dev.herokuapp.com/site/617923857ad4eeefea76d121"
                )

    async def test_remove_invalid_12_byte_hex_service_site_id(self):
        """Test remove invalid service site using its id which is 24 characters."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.delete(
                f"{self.base_url}/site/017923857ad4eeefea76d120"
            )
            self.assertEqual(404, responses.status_code)

    async def test_remvoe_invalid_service_site(self):
        """Test remove valid service site using 1 character as its id."""
        with self.assertRaises(bson.errors.InvalidId):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                await ac.delete(f"{self.base_url}/site/1")
