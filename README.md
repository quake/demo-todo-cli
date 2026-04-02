# demo-todo-cli

A simple command-line todo list manager written in Python.

## Usage

```bash
# Add a todo
python todo.py add "Buy groceries"

# List all todos
python todo.py list

# Mark a todo as done
python todo.py done 1

# Delete a todo
python todo.py delete 1

# Set a reminder on a todo
python todo.py remind 1 "2026-04-03 09:00"

# Clear a reminder from a todo
python todo.py remind 1 --clear

# List todos with upcoming reminders
python todo.py reminders
```

## Reminders

You can set a reminder datetime on any todo item. When listing todos, items with
reminders will show the reminder time. Overdue reminders are highlighted.

Use `reminders` to see only todos with upcoming (or overdue) reminders, sorted
by reminder time.

## Storage

Todos are stored in `~/.todos.json` by default. Use `--file` to specify a different path:

```bash
python todo.py --file ./my-todos.json add "Custom file"
```
