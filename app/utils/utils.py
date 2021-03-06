import requests


def get_access_to_api():
    res = requests.post(
        "https://wcg-apis.herokuapp.com/login", auth=("Chayapol", "Kp6192649")
    )
    access_token = res.json()["access_token"]
    return access_token


def fetch_url(URL, token=""):
    """Return a data that fetch from given url."""
    r = requests.get(URL, headers={"Authorization": "Bearer {}".format(token)})
    DATA = r.json()
    return DATA


def arranging_reservation_by_site_name(DATA):
    """Return reservation data that arranging by site name"""

    reservations = {}
    for item in DATA:
        site_name_key = item["site_name"]
        if site_name_key in reservations:
            reservations[site_name_key] = [*reservations[site_name_key], item]
        else:
            reservations[site_name_key] = [item]

    return reservations


def get_service_site_avaliable(data: dict, key: str):
    for i in data:
        if key == i:
            return i
    return None
