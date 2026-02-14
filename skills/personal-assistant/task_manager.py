#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path.home() / ".personal_assistant_tasks.json"

def load_tasks():
    return json.loads(TASKS_FILE.read_text()) if TASKS_FILE.exists() else []

def save_tasks(tasks):
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))

def add_task(description, priority="medium", due=None):
    tasks = load_tasks()
    tasks.append({"description": description, "priority": priority, "due": due, "done": False, "created": datetime.now().isoformat()})
    save_tasks(tasks)
    print(f"Added: {description}")

def list_tasks():
    tasks = [t for t in load_tasks() if not t["done"]]
    if not tasks:
        print("No pending tasks")
        return
    for i, t in enumerate(tasks, 1):
        print(f"{i}. [{t['priority']}] {t['description']}" + (f" (due: {t['due']})" if t['due'] else ""))

def complete_task(index):
    tasks = load_tasks()
    tasks[index]["done"] = True
    save_tasks(tasks)
    print(f"Completed: {tasks[index]['description']}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "add":
        add_task(sys.argv[2], sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--priority" else "medium", sys.argv[6] if len(sys.argv) > 6 and sys.argv[5] == "--due" else None)
    elif cmd == "list":
        list_tasks()
    elif cmd == "complete":
        complete_task(int(sys.argv[2]) - 1)
