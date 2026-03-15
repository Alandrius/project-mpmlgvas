import unittest
from datetime import date

from validation import (
    validate_phone,
    validate_email,
    validate_birthday,
    validate_note_title,
    validate_note_text,
    validate_tags,
)


class TestValidation(unittest.TestCase):
    def test_validate_phone_normalizes_local_format(self):
        valid, value = validate_phone("0501234567")
        self.assertTrue(valid)
        self.assertEqual(value, "+380501234567")

    def test_validate_phone_rejects_invalid_value(self):
        valid, message = validate_phone("123")
        self.assertFalse(valid)
        self.assertIn("Номер", message)

    def test_validate_phone_accepts_other_country_codes(self):
        valid, value = validate_phone("+12025551234")
        self.assertTrue(valid)
        self.assertEqual(value, "+12025551234")
        valid2, value2 = validate_phone("44 20 7123 4567")
        self.assertTrue(valid2)
        self.assertEqual(value2, "+442071234567")

    def test_validate_email_lowercases_valid_email(self):
        valid, value = validate_email("User.Name@Example.COM")
        self.assertTrue(valid)
        self.assertEqual(value, "user.name@example.com")

    def test_validate_email_rejects_double_dot(self):
        valid, message = validate_email("user..name@example.com")
        self.assertFalse(valid)
        self.assertIn("дві крапки", message)

    def test_validate_birthday_rejects_future_date(self):
        next_year = date.today().year + 1
        valid, message = validate_birthday(f"{next_year}-01-01")
        self.assertFalse(valid)
        self.assertIn("не може бути в майбутньому", message)

    def test_validate_birthday_accepts_valid_date(self):
        valid, value = validate_birthday("2000-02-29")
        self.assertTrue(valid)
        self.assertEqual(value, "2000-02-29")

    def test_validate_note_title_rejects_empty(self):
        valid, message = validate_note_title("   ")
        self.assertFalse(valid)
        self.assertIn("не може бути порожньою", message)

    def test_validate_note_text_rejects_empty(self):
        valid, message = validate_note_text("   ")
        self.assertFalse(valid)
        self.assertIn("не може бути порожнім", message)

    def test_validate_tags_normalizes_and_deduplicates(self):
        valid, tags = validate_tags([" Work ", "work", "Tag_1", ""])
        self.assertTrue(valid)
        self.assertEqual(tags, ["work", "tag_1"])

    def test_validate_tags_rejects_invalid_chars(self):
        valid, message = validate_tags(["tag@bad"])
        self.assertFalse(valid)
        self.assertIn("може містити лише", message)


if __name__ == "__main__":
    unittest.main()
