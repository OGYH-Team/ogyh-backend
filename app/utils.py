import requests
from functools import reduce

URL = ""
DATA = [
    {"site_name": "1", "name": "nice"},
    {"site_name": "1", "name": "kaopun"},
    {"site_name": "2", "name": "kuea"},
    {"site_name": "2", "name": "tae"},
    {"site_name": "3", "name": "ice"},
    {"site_name": "2", "name": "beam"},
    {"site_name": "2", "name": "korn"},
    {"site_name": "3", "name": "thorn"},
]


def get_reservation():
    # r = requests.get(URL)
    # get_data = r.json()

    reservations = {}

    for item in DATA:
        site_name_key = item['site_name']
        if site_name_key in reservations:
            reservations[site_name_key] = [*reservations[site_name_key], item]
        else:
            reservations[site_name_key] = [item]

    return reservations
