import sqlite3

def create_connection(db_file="database.db"):
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def creation_of_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            raw_message TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            log_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            FOREIGN KEY(log_id) REFERENCES log(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    """)

    conn.commit()

def insert_into_tables(conn, entries):
    cursor = conn.cursor()

    for entry in entries:

        cursor.execute(
            "INSERT INTO log (raw_message) VALUES (?)",
            (entry.raw,)
        )

        log_id = cursor.lastrowid  # id of inserted log

        cursor.execute(
            "INSERT INTO log_info (log_id, timestamp, level, message) VALUES (?, ?, ?, ?)",
            (log_id, entry.timestamp, entry.level.upper(), entry.message.lower())
        )

    conn.commit()
    cursor.close()
