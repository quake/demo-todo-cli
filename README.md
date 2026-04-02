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
```

## Storage

Todos are stored in `~/.todos.json` by default. Use `--file` to specify a different path:

```bash
python todo.py --file ./my-todos.json add "Custom file"
```
