import requests


def fetch_reservation(URL):
    """Get reservation URL."""
    r = requests.get(URL)
    DATA = r.json()
    return DATA


def get_reservation(DATA):
    """Arrange json format into dict."""
    reservations = {}
    for item in DATA:
        site_name_key = item['site_name']
        if site_name_key in reservations:
            reservations[site_name_key] = [*reservations[site_name_key], item]
        else:
            reservations[site_name_key] = [item]

    return reservations
