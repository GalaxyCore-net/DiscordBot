import json


def load_json(path):
    with open(path, encoding="utf-8") as infile:
        return json.load(infile)


def write_json(path, obj):
    with open(path, "w") as outfile:
        json.dump(obj, outfile, ensure_ascii=True, indent=4)


def save_config():
    write_json("config/config.json", config)


config = load_json("config/config.json")
