#!/usr/bin/env python3
"""A simple command-line todo list manager."""

import argparse
import json
import os
import sys

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
    """List all todo items, optionally filtered by status."""
    todos = load_todos(args.file)
    if not todos:
        print("No todos found.")
        return

    if args.done:
        todos = [t for t in todos if t["done"]]
    elif args.pending:
        todos = [t for t in todos if not t["done"]]

    if not todos:
        print("No matching todos found.")
        return

    for t in todos:
        status = "x" if t["done"] else " "
        print(f"  [{status}] #{t['id']}  {t['title']}")

    done_count = sum(1 for t in todos if t["done"])
    pending_count = len(todos) - done_count
    print(f"\n  {len(todos)} todo(s): {done_count} done, {pending_count} pending")


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
    list_parser = subparsers.add_parser("list", help="List all todos")
    list_filter = list_parser.add_mutually_exclusive_group()
    list_filter.add_argument("--done", action="store_true", help="Show only completed todos")
    list_filter.add_argument("--pending", action="store_true", help="Show only pending todos")

    # done
    done_parser = subparsers.add_parser("done", help="Mark a todo as done")
    done_parser.add_argument("id", type=int, help="ID of the todo to mark as done")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=int, help="ID of the todo to delete")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "delete": cmd_delete,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
