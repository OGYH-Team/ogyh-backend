from fastapi.testclient import TestClient

from ..main import app
import asynctest

client = TestClient(app)


class TestReservation(asynctest.TestCase):
    def test_read_main(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "hello from OGYH"}
