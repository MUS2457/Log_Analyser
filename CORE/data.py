from CORE import  parser, reader, module

def define_data(file_path):
    entries = []
    for line in reader.read_file(file_path):
        parsed = parser.parse_line(line)
        if parsed:
            entries.append(module.LogEntry.from_dict(parsed))
    return entries


