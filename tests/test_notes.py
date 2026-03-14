import unittest

from notes import NoteBook


class TestNotes(unittest.TestCase):
    def setUp(self):
        self.notebook = NoteBook()

    def test_add_edit_delete_note_flow(self):
        note = self.notebook.add_note("Task", "initial text")
        self.assertEqual(note.title, "Task")
        self.assertEqual(note.text, "initial text")

        updated = self.notebook.edit_note("Task", "updated text")
        self.assertEqual(updated.text, "updated text")

        self.notebook.delete_note("Task")
        self.assertEqual(len(self.notebook.data), 0)

    def test_add_duplicate_title_raises(self):
        self.notebook.add_note("Task", "one")
        with self.assertRaises(ValueError):
            self.notebook.add_note("Task", "two")

    def test_add_and_remove_tags_flow(self):
        self.notebook.add_note("Task", "text")
        note = self.notebook.add_tags("Task", ["Work", "work", "urgent"])
        self.assertEqual(note.tags, ["work", "urgent"])

        updated = self.notebook.remove_tag("Task", "work")
        self.assertEqual(updated.tags, ["urgent"])

    def test_remove_missing_tag_raises(self):
        self.notebook.add_note("Task", "text")
        with self.assertRaises(ValueError):
            self.notebook.remove_tag("Task", "missing")

    def test_search_and_sort_flow(self):
        self.notebook.add_note("Beta", "second", ["work"])
        self.notebook.add_note("Alpha", "first", ["home"])

        by_title = self.notebook.search_by_title("alp")
        by_tag = self.notebook.search_by_tag("work")
        sorted_notes = self.notebook.sort_by_title()

        self.assertEqual(len(by_title), 1)
        self.assertEqual(by_title[0].title, "Alpha")
        self.assertEqual(len(by_tag), 1)
        self.assertEqual(by_tag[0].title, "Beta")
        self.assertEqual([n.title for n in sorted_notes], ["Alpha", "Beta"])


if __name__ == "__main__":
    unittest.main()
