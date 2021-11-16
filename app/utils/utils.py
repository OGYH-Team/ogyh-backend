import requests


def fetch_url(URL):
    """Return a data that fetch from given url."""
    r = requests.get(URL)
    DATA = r.json()
    return DATA


def arranging_reservation_by_site_name(DATA):
    """Return reservation data that arranging by site name"""

    reservations = {}
    for item in DATA:
        site_name_key = item['site_name']
        if site_name_key in reservations:
            reservations[site_name_key] = [*reservations[site_name_key], item]
        else:
            reservations[site_name_key] = [item]

    return reservations


def get_cancellation(DATA, citizen_id):
    """Return the user if the citizen id is existed, otherwise return None."""
    for item in DATA.values():
        for user in item:
            cancel_id = user['citizen_id']
            if cancel_id == citizen_id:
                user['queue'] = ""
                return user
    return None


def get_service_site_avaliable(data: dict, key: str):
    for i in data:
        if(key == i):
            return i
    return None
