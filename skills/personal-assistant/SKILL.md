---
name: personal-assistant
description: Use this skill for daily life management tasks including scheduling, reminders, task tracking, and personal organization.
---

# personal-assistant

## Overview

This skill helps manage daily life activities, track tasks, and maintain personal organization.

## Instructions

### 1. Task Management

Use `task_manager.py` to:
- Add new tasks with priorities
- Mark tasks as complete
- List pending tasks
- Set due dates

### 2. Daily Planning

Use `daily_template.md` as a reference for:
- Morning routine checklist
- Daily goal setting
- Evening reflection prompts

### 3. Quick Notes

Use `quick_note.py` to:
- Capture quick thoughts
- Save ideas with timestamps
- Organize notes by category

## Usage Examples

**Adding a task:**
```bash
python task_manager.py add "Buy groceries" --priority high --due tomorrow
```

**Viewing tasks:**
```bash
python task_manager.py list
```

**Taking a quick note:**
```bash
python quick_note.py "Meeting idea: quarterly review format"
```
