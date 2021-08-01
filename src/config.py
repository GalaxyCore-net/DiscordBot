import json


def load_json(path):
    return json.load(open(path, "r"))


def write_json(path, obj):
    json.dump(obj, open(path, "w"))


config = load_json("config/config.json")
