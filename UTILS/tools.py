from datetime import datetime
from CORE.module import LogEntry
def search_by_level(conn):
    cursor = conn.cursor()

    while True:
        level_user = input("Please enter the level of log or 'exit' to quit: ").strip()

        if level_user.lower() == "exit":
            print("Quitting...")
            return {}

        cursor.execute("""
            SELECT log.created_at,
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

        results = {}

        for row in rows:
            created_at = row["created_at"]
            timestamp = row["timestamp"]
            level = row["level"]
            message = row["message"]

            dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

            results[dt] = LogEntry(created_at, timestamp, level, message)

        print(f"\nRESULTS FOR LEVEL: {level_user.upper()}")
        for dt, info in results.items():
            print(f"{dt} : {info}")

        return results




