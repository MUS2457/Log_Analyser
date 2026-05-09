from datetime import datetime
from CORE.module import LogEntry
import re
from DATABASE import summary_json

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

def search_by_keyword(conn):
        cursor = conn.cursor()

        while True:
            print("SEARCH BY KEYWORD TOOL")
            user_keyword = input("Please enter the keyword of log or 'exit' to quit: ").strip()

            if user_keyword.lower() == "exit":
                print("Quitting...")
                break

            cursor.execute("""SELECT log.created_at,
                                     log.raw_message,
                                     log_info.timestamp,
                                     log_info.level,
                                     log_info.message
                                     FROM log 
                                     JOIN log_info ON log.id = log_info.log_id
                                     WHERE LOWER(raw_message) LIKE ?
            """, (("%" + user_keyword.lower() + "%"),
            ))

            rows = cursor.fetchall()

            if not rows:
                print("No entries found for that keyword.")
                continue

            results = get_results(rows)

            print(f"\nRESULTS FOR KEYWORD: {user_keyword}, {len(results)} entries found.")
            for dt, info in results.items():
                print(f"{dt} : {info}")

            return results


def view_summaries_based_on_date():
    data = summary_json.load_summary()

    if not data:
        print("No data exists , run the program at least once.")
        return {}

    while True:
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        print("VIEW SUMMARY BY DATE")
        user_date = input("Please enter the date of log or 'exit' to quit: ").strip()

        if user_date.lower() == "exit":
            print("Quitting...")
            break

        elif not re.match(pattern, user_date):
            print("Invalid date format.")
            continue

        results = {}

        for date, summaries in data.items():
            if date.startswith(user_date):
                results[date] = summaries

        if not results:
            print("No summaries found for that date.")
            continue

        print(f"\nRESULTS FOR DATE: {user_date} ,{len(results)} summaries found.")
        for date, summaries in results.items():
            print(f"{date} : {summaries}")

        return results



