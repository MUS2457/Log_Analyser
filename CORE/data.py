import parser
import module

def define_data(path_log):
    entries = []

    try:
        with open(path_log, "r") as logs:
            for line in logs:
                entry_dict = parser.parse_line(line)

                if entry_dict:
                    entries.append(module.LogEntry.from_dict(entry_dict))

        return entries

    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        return None


