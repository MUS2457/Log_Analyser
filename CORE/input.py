import os

def get_file_path() :
    extensions = [".log", ".txt", ".out"]
    while True :
        file_path = input("Enter the file path or 'exit' to quit : ").strip()

        if file_path.lower() == 'exit' :
            print("Goodbye")
            break

        elif os.path.exists(file_path) :
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            _, file_extension = os.path.splitext(file_name)
            if file_extension.lower() in extensions and file_size > 0 :
                return file_path
            else :
                print("This file is not a log file")
                continue

        else :
            print("Please enter a valid file path")

