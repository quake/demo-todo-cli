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

Todos are persisted as JSON in `~/.todos.json` by default. The storage layer (`storage.py`) provides:

- **Atomic writes** — writes to a temporary file first, then renames, preventing corruption on crashes
- **Auto-directory creation** — parent directories are created automatically if they don't exist
- **Timestamps** — each todo records a `created_at` timestamp in UTC ISO-8601 format
- **Data validation** — rejects files that don't contain a JSON array

Use `--file` to specify a different path:

```bash
python todo.py --file ./my-todos.json add "Custom file"
```

## Testing

```bash
python3 -m unittest test_storage -v
```
