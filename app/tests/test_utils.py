from app.utils import utils
from app.utils.sample_reservations import sample_reservations
import unittest
import requests


class TestUtils(unittest.TestCase):


    def test_fetch_url(self):
        URL = "https://wcg-apis.herokuapp.com/reservations"
        res = utils.fetch_url(URL=URL)
        self.assertEqual(list, type(res))
    
    def test_fetch_invalid_url(self):
        URL = "https://wcg-apis.herokuapp.com/reservations"
        res = utils.fetch_url(URL=URL)
        self.assertEqual(list, type(res))

    def test_arraging_reservation(self):
        reservations = utils.arranging_reservation_by_site_name(sample_reservations)
        self.assertNotEqual(reservations, sample_reservations)

