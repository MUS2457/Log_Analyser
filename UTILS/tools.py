from datetime import datetime
from CORE.module import LogEntry
import re

def get_results(rows):
    results = {}
    for row in rows:
        created_at = row["created_at"]
        timestamp = row["timestamp"]
        level = row["level"]
        message = row["message"]
        raw_message = row["raw_message"]

        dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

        results[dt] = LogEntry(timestamp, level, message, raw_message)

    return results

def search_by_level(conn):
    cursor = conn.cursor()

    while True:
        level_user = input("Please enter the level of log or 'exit' to quit: ").strip()

        if level_user.lower() == "exit":
            print("Quitting...")
            return {}

        cursor.execute("""
            SELECT log.created_at,
                   log.raw_message,
                   log_info.timestamp,
                   log_info.level,
                   log_info.message
            FROM log
            JOIN log_info ON log.id = log_info.log_id
            WHERE log_info.level = ?
        """, (level_user.upper(),))

        rows = cursor.fetchall()

        if not rows:
            print("No entries found for that level.")
            continue

        results = get_results(rows)

        print(f"\nRESULTS FOR LEVEL: {level_user.upper()} , {len(results)} entries found")
        for dt, info in results.items():
            print(f"{dt} : {info}")

        return results

def search_by_date(conn):
    cursor = conn.cursor()

    while True:
        pattern = r"^\d{4}-\d{2}-\d{2}$"

        date = input("Please enter the date of log "
        "you would like to search in ('YYYY-MM-DD') or 'exit' to quit: ").strip()

        if date.lower() == "exit":
            print("Quitting...")
            break

        elif not re.match(pattern, date):
            print("Invalid date format.")
            continue

        cursor.execute("""SELECT log.created_at,
                                 log.raw_message,
                                 log_info.timestamp,
                                 log_info.level,
                                 log_info.message
                                 FROM log 
                                JOIN log_info ON log.id = log_info.log_id
                                WHERE strftime('%Y-%m-%d', log.created_at) = ?
        """, (date,))

        rows = cursor.fetchall()

        if not rows:
            print("No entries found for that date.")
            continue

        results = get_results(rows)

        print(f"\nRESULTS FOR DATE: {date} ,{len(results)} entries found.")
        for dt, info in results.items():
            print(f"{dt} : {info}")

        return results


def search_by_date_range(conn):
    cursor = conn.cursor()

    while True:
        print("SEARCH BY DATE RANGE TOOL")
        pattern = r"^\d{4}-\d{2}-\d{2}$"

        date_1 = input("Please enter first date in ('YYYY-MM-DD') or 'exit' to quit: ").strip()

        if date_1.lower() == "exit":
            print("Quitting...")
            break

        date_2 = input("Please enter second date in ('YYYY-MM-DD')").strip()

        if not re.match(pattern, date_2) or not re.match(pattern, date_1)  or date_1 == date_2:
            print("Invalid date format.")
            continue

        cursor.execute("""SELECT log.created_at,
                                 log.raw_message,
                                 log_info.timestamp,
                                 log_info.level,
                                 log_info.message
                                 FROM log 
                                 JOIN log_info ON log.id = log_info.log_id
                                 WHERE strftime('%Y-%m-%d', log.created_at) 
                                 BETWEEN  ?
                                 AND      ?
        """, (date_1, date_2))

        rows = cursor.fetchall()

        if not rows:
            print("No entries found for that date range.")
            continue

        results = get_results(rows)

        print(f"\nRESULTS FOR DATE RANGE BETWEEN '{date_1}' AND '{date_2}' ,{len(results)} entries found.")
        for dt, info in results.items():
            print(f"{dt} : {info}")

        return results

