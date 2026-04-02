"""Persistent JSON file storage for the todo CLI.

Provides a Storage class that handles reading and writing todos to a JSON file
with atomic writes, automatic directory creation, and data integrity checks.
"""

import json
import os
import tempfile
from datetime import datetime, timezone


class Storage:
    """Manages persistent JSON file storage for todo items."""

    def __init__(self, filepath):
        self.filepath = filepath

    def _ensure_directory(self):
        """Create the parent directory if it doesn't exist."""
        directory = os.path.dirname(self.filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def load(self):
        """Load todos from the JSON file.

        Returns an empty list if the file doesn't exist or is empty.
        Raises ValueError if the file contains invalid JSON.
        """
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValueError(
                    f"Expected a JSON array in {self.filepath}, "
                    f"got {type(data).__name__}"
                )
            return data

    def save(self, todos):
        """Save todos to the JSON file using atomic write.

        Writes to a temporary file first, then renames it to the target path.
        This prevents data corruption if the process is interrupted mid-write.
        """
        self._ensure_directory()
        directory = os.path.dirname(self.filepath) or "."
        fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(todos, f, indent=2)
                f.write("\n")
            os.replace(tmp_path, self.filepath)
        except BaseException:
            # Clean up the temp file on any failure
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise


def make_todo(todo_id, title):
    """Create a new todo dict with an ID, title, and timestamp."""
    return {
        "id": todo_id,
        "title": title,
        "done": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
