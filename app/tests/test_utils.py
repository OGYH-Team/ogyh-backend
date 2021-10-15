from .. import utils
import unittest


class TestUtils(unittest.TestCase):

    user1 = {
        "citizen_id": 1234567890123,
        "site_name": "ogyh1",
        "vaccine_name": "",
        "timestamp": "",
        "queue": ""
    }
    user2 = {
        "citizen_id": 1234567890123,
        "site_name": "ogyh1",
        "vaccine_name": "",
        "timestamp": "",
        "queue": ""
    }
    user3 = {
        "citizen_id": 1234567890123,
        "site_name": "ogyh2",
        "vaccine_name": "",
        "timestamp": "",
        "queue": ""
    }
    user4 = {
        "citizen_id": 1234567890123,
        "site_name": "ogyh2",
        "vaccine_name": "",
        "timestamp": "",
        "queue": ""
    }

    users = [user1, user2, user3, user4]

    URL = ""

    def test_get_reservation(self):
        reservations = utils.get_reservation(self.users)
        self.assertEqual(2, len(reservations))
