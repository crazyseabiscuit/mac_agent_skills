#!/usr/bin/env python3
import sys
from datetime import datetime
from pathlib import Path

NOTES_FILE = Path.home() / ".personal_assistant_notes.txt"

def add_note(content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(NOTES_FILE, "a") as f:
        f.write(f"[{timestamp}] {content}\n")
    print(f"Note saved: {content}")

if __name__ == "__main__":
    add_note(" ".join(sys.argv[1:]))
