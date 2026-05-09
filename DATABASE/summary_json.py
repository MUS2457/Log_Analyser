import json
from datetime import datetime

FILE_NAME = 'summary.json'

def save_summary(summary):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(FILE_NAME) as json_file:
            data = json.load(json_file)

    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        data = {}

    data[current_time] = summary # set a unique key for history and add powerful tools

    with open(FILE_NAME, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def load_summary():
    try:
        with open(FILE_NAME) as json_file:
            data = json.load(json_file)
            return data

    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        return {}


