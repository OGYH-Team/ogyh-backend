import requests
URL = ""


def get_reservation():
    r = requests.get(URL)
    get_data = r.json()
    reservations = separate_reservation_by_site_name(get_data)
    return reservations


def separate_reservation_by_site_name(reservations: list):
    return {}
