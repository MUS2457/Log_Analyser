import re
from datetime import datetime

TIMESTAMP_PATTERNS = [
    (r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", "%Y-%m-%d %H:%M:%S"),
    (r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}", "%Y/%m/%d %H:%M:%S"),
    (r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}", "%d-%m-%Y %H:%M:%S"),
    (r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", "%d/%m/%Y %H:%M:%S"),
]    # regex

def extract_timestamp(line):
    for pattern, fmt in TIMESTAMP_PATTERNS:
        match = re.search(pattern, line)  #search inside the bag for that shape
        if match:
            try:
                return datetime.strptime(match.group(), fmt)
            except ValueError:
                continue
    return None

def extract_level(line):
    log_levels = [
        "CRITICAL", "ERROR",
        "WARNING", "INFO",
        "DEBUG", "NOTSET",
        "FATAL", "TRACE",
        "NOTICE", "ALERT",
           "EMERGENCY"
    ]

    for level in log_levels:
        result = re.search(level, line)

        if result:
            return level

    return None

def extract_message(line, level):
    message = line.split(level, 1)[1].strip()  # cut the line at the level, take what's after [1] is like index, and remove extra spaces

    if message:
        return message

    return None


def parse_line(line):
    timestamp = extract_timestamp(line)
    level = extract_level(line)
    message = extract_message(line, level)

    if timestamp and level and message:

        return {"timestamp": timestamp, "level": level, "message": message, "raw": line}

    return None