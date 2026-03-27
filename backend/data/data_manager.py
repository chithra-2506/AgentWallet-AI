# data/data_manager.py

import json
import os

DATA_FILE = "data/user_data.json"


def _ensure_file():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"history": []}, f)


def load_data():
    _ensure_file()
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_transaction(amount, category):
    data = load_data()

    data["history"].append({
        "amount": amount,
        "category": category
    })

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_history():
    data = load_data()
    return data.get("history", [])


def clear_history():
    with open(DATA_FILE, "w") as f:
        json.dump({"history": []}, f)
