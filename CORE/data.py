from CORE import  parser, reader

def define_data(file_path):
    entries = []
    for line in reader.read_file(file_path):
        parsed = parser.parse_line(line)
        if parsed:
            entries.append(parsed)
    return entries


