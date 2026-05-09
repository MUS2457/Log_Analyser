import sys
from ANALYSIS.analyser import LogAnalyser
from CORE.data import define_data
from CORE.input import get_file_path
from DATABASE.sql import create_connection, creation_of_tables, insert_into_tables
from UTILS import tools
from DATABASE import summary_json


def load_logs_from_file():
    path = get_file_path()    #C:\Users\musta\Music\am.log my test scrip
    if not path:
        return None

    entries = define_data(path)
    if entries is None:
        print("Error reading file.")
        return None

    print(f"\nLoaded {len(entries)} log entries.")
    return entries


def analyse_logs(entries):
    analyser = LogAnalyser(entries)
    summary = analyser.summary_report()

    print("\n=== SUMMARY REPORT ===")
    for key, value in summary.items():
        print(f"{key}: {value}")

    save = input("Would you like to save this summary? (y): ").strip().lower()
    if save == "y":
        summary_json.save_summary(summary)
        print("Summary saved successfully.")

    return summary


def insert_into_db(entries):
    confirm = input("Would you like to continue? (y): ").strip().lower()
    if confirm == "y":
        conn = create_connection()
        creation_of_tables(conn)
        insert_into_tables(conn, entries)
        print("Logs inserted into database successfully.")

    print("Log entry insertion canceled.")
    return


def search_in_db():
    conn = create_connection()
    creation_of_tables(conn)

    while True:
        print("\n=== DATABASE SEARCH MENU ===")
        print("1. Search by level")
        print("2. Search by date")
        print("3. Search by date range")
        print("4. Search by keyword")
        print("5. View saved summaries by date")
        print("6. Back to main menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            tools.search_by_level(conn)
        elif choice == "2":
            tools.search_by_date(conn)
        elif choice == "3":
            tools.search_by_date_range(conn)
        elif choice == "4":
            tools.search_by_keyword(conn)
        elif choice == "5":
            tools.view_summaries_based_on_date()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


def main():
    entries = None

    while True:
        print("\n=== LOG ANALYSER MAIN MENU BY RAIJIN_CODE ===")
        print("1. Load logs from file")
        print("2. Analyse logs")
        print("3. Insert logs into database")
        print("4. Search database")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            entries = load_logs_from_file()

        elif choice == "2":
            if entries is None:
                print("Load logs first.")
            else:
                analyse_logs(entries)

        elif choice == "3":
            if entries is None:
                print("Load logs first.")
            else:
                insert_into_db(entries)

        elif choice == "4":
            search_in_db()

        elif choice == "5":
            print("Goodbye.")
            sys.exit()

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
