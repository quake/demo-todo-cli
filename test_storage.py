"""Tests for the persistent JSON storage module."""

import json
import os
import tempfile
import unittest

from storage import Storage, make_todo


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.filepath = os.path.join(self.tmpdir, "test_todos.json")
        self.store = Storage(self.filepath)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)
        os.rmdir(self.tmpdir)

    def test_load_nonexistent_file_returns_empty(self):
        self.assertEqual(self.store.load(), [])

    def test_load_empty_file_returns_empty(self):
        with open(self.filepath, "w") as f:
            f.write("")
        self.assertEqual(self.store.load(), [])

    def test_save_and_load_roundtrip(self):
        todos = [make_todo(1, "Buy groceries"), make_todo(2, "Walk the dog")]
        self.store.save(todos)
        loaded = self.store.load()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["title"], "Buy groceries")
        self.assertEqual(loaded[1]["title"], "Walk the dog")

    def test_save_creates_parent_directory(self):
        nested_path = os.path.join(self.tmpdir, "sub", "dir", "todos.json")
        store = Storage(nested_path)
        store.save([make_todo(1, "Test")])
        loaded = store.load()
        self.assertEqual(len(loaded), 1)
        # Cleanup nested dirs
        os.unlink(nested_path)
        os.rmdir(os.path.join(self.tmpdir, "sub", "dir"))
        os.rmdir(os.path.join(self.tmpdir, "sub"))

    def test_save_atomic_no_temp_files_left(self):
        self.store.save([make_todo(1, "Test")])
        files = os.listdir(self.tmpdir)
        # Only the target file should exist, no .tmp leftovers
        self.assertEqual(files, ["test_todos.json"])

    def test_load_invalid_json_raises(self):
        with open(self.filepath, "w") as f:
            f.write("not json")
        with self.assertRaises(json.JSONDecodeError):
            self.store.load()

    def test_load_non_array_raises_value_error(self):
        with open(self.filepath, "w") as f:
            json.dump({"key": "value"}, f)
        with self.assertRaises(ValueError):
            self.store.load()

    def test_save_appends_trailing_newline(self):
        self.store.save([make_todo(1, "Test")])
        with open(self.filepath, "r") as f:
            content = f.read()
        self.assertTrue(content.endswith("\n"))


class TestMakeTodo(unittest.TestCase):
    def test_creates_todo_with_required_fields(self):
        todo = make_todo(1, "Test task")
        self.assertEqual(todo["id"], 1)
        self.assertEqual(todo["title"], "Test task")
        self.assertFalse(todo["done"])
        self.assertIn("created_at", todo)

    def test_created_at_is_iso_format(self):
        todo = make_todo(1, "Test")
        # Should be parseable as ISO format and contain timezone info
        self.assertIn("T", todo["created_at"])
        self.assertTrue(todo["created_at"].endswith("+00:00"))


if __name__ == "__main__":
    unittest.main()
