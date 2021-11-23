from app.main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asynctest
from unittest.case import skip


class TestAuthentication(asynctest.TestCase):
    async def setUp(self) -> None:
        self.client = TestClient(app)
        self.base_url = "/login"
        self.read_user_url = '/users/me'
        self.valid_user = {
            "username": "Tester",
            "password": "tester123"
        }
        self.invalid_user ={
            "username": "Faker",
            "password": "Fakepassword"
        }

    async def test_login_with_valid_user(self):
        """Test login the valid user."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.post(f"{self.base_url}", data=self.valid_user)
        self.assertEqual(201, responses.status_code)
        self.assertIn('access_token', responses.json())

    async def test_login_with_wrong_password(self):
        """Test login with valid user but wrong password."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            self.valid_user['password'] = 'Wrong password'
            responses = await ac.post(f"{self.base_url}", data=self.valid_user)
        self.assertEqual(404, responses.status_code)
        self.assertEqual("Incorrect password", responses.json()['detail'])

    async def test_login_missing_username(self):
        """Test login without username."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            del self.valid_user['username']
            responses = await ac.post(f"{self.base_url}", data=self.valid_user)
        self.assertEqual(422, responses.status_code)
        self.assertEqual(responses.json()['detail'][0]['loc'], ['body', 'username'])
    
    async def test_login_missing_password(self):
        """Test login without password."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            del self.valid_user['password']
            responses = await ac.post(f"{self.base_url}", data=self.valid_user)
        self.assertEqual(422, responses.status_code)
        self.assertEqual(responses.json()['detail'][0]['loc'], ['body', 'password'])

    async def test_login_with_invalid_user(self):
        """Test login the invalid user."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            responses = await ac.post(f"{self.base_url}", data=self.invalid_user)
        self.assertEqual(404, responses.status_code)
        self.assertEqual("Invalid Credentials", responses.json()['detail'])

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






