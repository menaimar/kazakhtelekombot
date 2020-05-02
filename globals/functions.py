import json
import requests
from difflib import get_close_matches
from aiogram import types


def is_int(n) -> bool:
    try:
        int(n)
    except ValueError:
        return False
    return True


def open_json(fp: str) -> dict:
    return json.load(open(fp, encoding="utf-8"))


def ktcheck(req: dict):
    return requests.post("https://telecom.kz/api/v1.0/main/videomonitoring/check_technical_availability",
        headers={"referer": "https://telecom.kz/ru/common/cctv-home", "accept": "application/json"},json=req
    ).json()["result"]


def create_reply_markup(m: list):
    if m is None:
        return None

    markup = types.InlineKeyboardMarkup()
    for i in m:
        markup.row(*list(map(lambda x: types.InlineKeyboardButton(x, callback_data=x), i)))

    return markup


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
