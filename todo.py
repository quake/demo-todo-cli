#!/usr/bin/env python3
"""A simple command-line todo list manager."""

import argparse
import json
import os
import sys
from datetime import datetime

DEFAULT_FILE = os.path.join(os.path.expanduser("~"), ".todos.json")


def load_todos(filepath):
    """Load todos from a JSON file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)


def save_todos(filepath, todos):
    """Save todos to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(todos, f, indent=2)


def cmd_add(args):
    """Add a new todo item."""
    todos = load_todos(args.file)
    next_id = max((t["id"] for t in todos), default=0) + 1
    todo = {"id": next_id, "title": args.title, "done": False}
    todos.append(todo)
    save_todos(args.file, todos)
    print(f"Added todo #{next_id}: {args.title}")


def cmd_list(args):
    """List all todo items."""
    todos = load_todos(args.file)
    if not todos:
        print("No todos found.")
        return
    now = datetime.now()
    for t in todos:
        status = "x" if t["done"] else " "
        reminder_str = ""
        if t.get("reminder") and not t["done"]:
            reminder_dt = datetime.fromisoformat(t["reminder"])
            overdue = " OVERDUE" if reminder_dt <= now else ""
            reminder_str = f"  [remind: {reminder_dt.strftime('%Y-%m-%d %H:%M')}{overdue}]"
        print(f"  [{status}] #{t['id']}  {t['title']}{reminder_str}")


def cmd_done(args):
    """Mark a todo item as done."""
    todos = load_todos(args.file)
    for t in todos:
        if t["id"] == args.id:
            t["done"] = True
            save_todos(args.file, todos)
            print(f"Marked todo #{args.id} as done.")
            return
    print(f"Todo #{args.id} not found.", file=sys.stderr)
    sys.exit(1)


def cmd_delete(args):
    """Delete a todo item by its ID."""
    todos = load_todos(args.file)
    original_len = len(todos)
    todos = [t for t in todos if t["id"] != args.id]
    if len(todos) == original_len:
        print(f"Todo #{args.id} not found.", file=sys.stderr)
        sys.exit(1)
    save_todos(args.file, todos)
    print(f"Deleted todo #{args.id}.")


def cmd_remind(args):
    """Set a reminder datetime on a todo item."""
    if not args.clear and args.datetime is None:
        print(
            "Please provide a datetime in 'YYYY-MM-DD HH:MM' format, or use --clear.",
            file=sys.stderr,
        )
        sys.exit(1)
    todos = load_todos(args.file)
    for t in todos:
        if t["id"] == args.id:
            if args.clear:
                t.pop("reminder", None)
                save_todos(args.file, todos)
                print(f"Cleared reminder for todo #{args.id}.")
                return
            try:
                reminder_dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M")
            except ValueError:
                print(
                    "Invalid datetime format. Use 'YYYY-MM-DD HH:MM'.",
                    file=sys.stderr,
                )
                sys.exit(1)
            t["reminder"] = reminder_dt.isoformat()
            save_todos(args.file, todos)
            print(
                f"Set reminder for todo #{args.id}: {reminder_dt.strftime('%Y-%m-%d %H:%M')}"
            )
            return
    print(f"Todo #{args.id} not found.", file=sys.stderr)
    sys.exit(1)


def cmd_reminders(args):
    """List todos that have reminders, highlighting overdue ones."""
    todos = load_todos(args.file)
    reminders = [t for t in todos if t.get("reminder") and not t["done"]]
    if not reminders:
        print("No upcoming reminders.")
        return
    now = datetime.now()
    reminders.sort(key=lambda t: t["reminder"])
    for t in reminders:
        reminder_dt = datetime.fromisoformat(t["reminder"])
        overdue = " [OVERDUE]" if reminder_dt <= now else ""
        print(
            f"  [ ] #{t['id']}  {t['title']}  -- reminder: {reminder_dt.strftime('%Y-%m-%d %H:%M')}{overdue}"
        )


def main():
    parser = argparse.ArgumentParser(description="A simple todo list manager.")
    parser.add_argument(
        "--file",
        default=DEFAULT_FILE,
        help=f"Path to the todos JSON file (default: {DEFAULT_FILE})",
    )
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("title", help="Title of the todo item")

    # list
    subparsers.add_parser("list", help="List all todos")

    # done
    done_parser = subparsers.add_parser("done", help="Mark a todo as done")
    done_parser.add_argument("id", type=int, help="ID of the todo to mark as done")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=int, help="ID of the todo to delete")

    # remind
    remind_parser = subparsers.add_parser(
        "remind", help="Set a reminder on a todo"
    )
    remind_parser.add_argument(
        "id", type=int, help="ID of the todo to set a reminder for"
    )
    remind_parser.add_argument(
        "datetime",
        nargs="?",
        default=None,
        help="Reminder datetime in 'YYYY-MM-DD HH:MM' format",
    )
    remind_parser.add_argument(
        "--clear", action="store_true", help="Clear the reminder from the todo"
    )

    # reminders
    subparsers.add_parser("reminders", help="List todos with upcoming reminders")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "delete": cmd_delete,
        "remind": cmd_remind,
        "reminders": cmd_reminders,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
