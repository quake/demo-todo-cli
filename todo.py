#!/usr/bin/env python3
"""A simple command-line todo list manager."""

import argparse
import os
import sys

from storage import Storage, make_todo

DEFAULT_FILE = os.path.join(os.path.expanduser("~"), ".todos.json")


def cmd_add(args):
    """Add a new todo item."""
    store = Storage(args.file)
    todos = store.load()
    next_id = max((t["id"] for t in todos), default=0) + 1
    todo = make_todo(next_id, args.title)
    todos.append(todo)
    store.save(todos)
    print(f"Added todo #{next_id}: {args.title}")


def cmd_list(args):
    """List all todo items."""
    store = Storage(args.file)
    todos = store.load()
    if not todos:
        print("No todos found.")
        return
    for t in todos:
        status = "x" if t["done"] else " "
        print(f"  [{status}] #{t['id']}  {t['title']}")


def cmd_done(args):
    """Mark a todo item as done."""
    store = Storage(args.file)
    todos = store.load()
    for t in todos:
        if t["id"] == args.id:
            t["done"] = True
            store.save(todos)
            print(f"Marked todo #{args.id} as done.")
            return
    print(f"Todo #{args.id} not found.", file=sys.stderr)
    sys.exit(1)


def cmd_delete(args):
    """Delete a todo item by its ID."""
    store = Storage(args.file)
    todos = store.load()
    original_len = len(todos)
    todos = [t for t in todos if t["id"] != args.id]
    if len(todos) == original_len:
        print(f"Todo #{args.id} not found.", file=sys.stderr)
        sys.exit(1)
    store.save(todos)
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
    subparsers.add_parser("list", help="List all todos")

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
