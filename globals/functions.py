import json
import requests
from difflib import get_close_matches


def is_int(n) -> bool:
    try:
        int(n)
    except ValueError:
        return False
    return True


def open_json(fp: str) -> dict:
    return json.load(open(fp))


def ktcheck(req:dict):
    return True


def create_reply_markup(m):
    pass


def get_cities(region):
    return requests.get(
        f"https://telecom.kz/api/v1.0/main/videomonitoring/get_towns?serverId={region}",
        headers={"referer": "https://telecom.kz/ru/common/cctv-home", "accept": "application/json"}
    ).json()


def get_streets(region, city):
    return requests.get(
        f"https://telecom.kz/api/v1.0/main/videomonitoring/get_streets?serverId={region}&town_id={city}",
        headers={"referer": "https://telecom.kz/ru/common/cctv-home", "accept": "application/json"}
    ).json()
