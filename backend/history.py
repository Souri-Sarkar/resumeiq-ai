import json
import os

HISTORY_FILE = "analysis_history.json"

def save_analysis(data):

    history = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    history.append(data)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

def get_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)