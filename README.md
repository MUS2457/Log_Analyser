# Log Analyser

A lightweight, modular tool for processing and understanding log files.  
Designed to handle large files safely, analyse patterns, and store results for later search.

This project reflects my approach to backend development:  
clean architecture, modular design, and practical problem‑solving.


## Why I Built This

For fun == challenge.

I wanted a tool that could:

- read large log files safely by processing one line at a time, extracting structured data, and adding each entry only after parsing (avoiding loading the entire file at once)
- extract structured information from raw text
- generate useful summaries
- store logs in a database
- search them quickly using different filters

Most log tools are heavy or over‑engineered.  
This one is simple, fast, and easy to extend.

---

## What I Learned

### • Streaming file processing with `yield`
I learned how to process large log files safely by reading them one line at a time using a generator.  
This pattern avoids loading the entire file into memory.  
Each line is yielded, parsed, converted into a structured entry, and then the reader continues to the next line.  
This was my first real use of streaming architecture — *tanoshikatta*.

### • Practical use of regular expressions (regex)
I used regex to extract timestamps, log levels, and messages from raw log lines.  
This project helped me understand how to design patterns, test them, and use them efficiently inside a parser.

---

## Core Features

### Memory‑Safe Log Loading
Processes files line‑by‑line using a generator.  
Safe for large logs (I thought about this after facing some huge logs with hundreds of thousands of lines).

### Structured Parsing
Each log line becomes a `LogEntry` object with:
- timestamp  
- level  
- message  
- raw text  

### Summary Analysis
Generates a report including:
- total entries  
- counts per level  
- earliest and latest timestamps  

Summaries can be saved as JSON.

### SQLite Storage
Logs can be inserted into a local SQLite database  
(used SQL for faster search and the built‑in features it provides).

### Search Tools
Search logs by:
- level  
- date  
- date range  
- keyword  

Also supports viewing saved summaries (using the dates saved in JSON).

---

## Project Structure
CORE/
reader.py         # streaming file reader (uses yield)
parser.py         # regex-based line parser
data.py           # define_data() pipeline
module.py         # LogEntry class

ANALYSIS/
analyser.py       # summary logic and report generation
analyser_helper   # functions that support analyser class methods

DATABASE/
sql.py            # SQLite connection, table creation, inserts
summary_json.py   # save/load summary reports as JSON

UTILS/
tools.py          # search utilities for database queries

main.py             # CLI entry point and menu flow

## How to Run

1. Make sure you have Python 3.10+ installed.

2. Clone the project:
   git clone <your-repo-url>

3. Navigate into the project folder:
   cd log-analyser

4. Run the program:
   python main.py

You will see a simple CLI menu that lets you:
- load logs
- analyse them
- save summaries
- insert into the database
- search stored logs

