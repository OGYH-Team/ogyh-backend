from app.main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
import requests_mock
import asynctest
from unittest.case import skip


class TestAuthentication(asynctest.TestCase):
    async def setUp(self) -> None:
        self.client = TestClient(app)
        self.base_url = "/login"
        self.read_user_url = "/users/me"
        self.valid_user = {"username": "Tester", "password": "tester123"}
        self.invalid_user = {"username": "Faker", "password": "Fakepassword"}

    async def test_login_with_valid_user(self):
        """Test login the valid user."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.post(f"{self.base_url}", data=self.valid_user)
        self.assertEqual(201, responses.status_code)
        self.assertIn("access_token", responses.json())

    async def test_login_with_wrong_password(self):
        """Test login with valid user but wrong password."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            self.valid_user["password"] = "Wrong password"
            responses = await ac.post(f"{self.base_url}", data=self.valid_user)
        self.assertEqual(404, responses.status_code)
        self.assertEqual("Incorrect password", responses.json()["detail"])

    async def test_login_missing_username(self):
        """Test login without username."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            del self.valid_user["username"]
            responses = await ac.post(f"{self.base_url}", data=self.valid_user)
        self.assertEqual(422, responses.status_code)
        self.assertEqual(responses.json()["detail"][0]["loc"], ["body", "username"])

    async def test_login_missing_password(self):
        """Test login without password."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            del self.valid_user["password"]
            responses = await ac.post(f"{self.base_url}", data=self.valid_user)
        self.assertEqual(422, responses.status_code)
        self.assertEqual(responses.json()["detail"][0]["loc"], ["body", "password"])

    async def test_login_with_invalid_user(self):
        """Test login the invalid user."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.post(f"{self.base_url}", data=self.invalid_user)
        self.assertEqual(404, responses.status_code)
        self.assertEqual("Invalid Credentials", responses.json()["detail"])

    async def test_add_service_site(self):
        """Test valid user add the service site to database."""
        valid_service_site = {
            "name": "TEST2",
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
        async with AsyncClient(app=app, base_url="http://test") as ac:
            login_responses = await ac.post(f"{self.base_url}", data=self.valid_user)
            access_token = login_responses.json()["access_token"]
            with requests_mock.Mocker() as rm:
                rm.post(f"/api/site", json=valid_service_site)
                response = await ac.post(
                    "/api/site",
                    json=valid_service_site,
                    headers={"Authorization": "Bearer {}".format(access_token)},
                )
                self.assertEqual(201, response.status_code)

    @skip("Not complete")
    async def test_read_user_when_login(self):
        """Test get current user while login."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await ac.post(f"{self.base_url}", data=self.valid_user)
            responses = await ac.get(f"{self.read_user_url}")
        self.assertEqual(200, responses.status_code)
        self.assertEqual("", responses.text)

    @skip("Not complete")
    async def test_read_user_without_login(self):
        """Test get current user witout login."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.get(f"{self.read_user_url}")
        self.assertEqual(404, responses.status_code)
        self.assertEqual("", responses.json())
