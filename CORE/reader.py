def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError): # I will use Exception later on (generalize error), stop py from barking
        return
