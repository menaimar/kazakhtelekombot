import json


def open_json(fp: str) -> dict:
    return json.load(open(fp))
