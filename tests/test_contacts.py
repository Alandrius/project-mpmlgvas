import unittest
from datetime import date

from contacts import AddressBook, Contact


class TestContacts(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()

    def test_add_find_delete_contact_flow(self):
        contact = Contact("Ivan", phone="+380501234567", email="ivan@example.com")
        self.book.add_contact(contact)

        found = self.book.find_contact("ivan")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Ivan")

        deleted = self.book.delete_contact("Ivan")
        self.assertIsNotNone(deleted)
        self.assertIsNone(self.book.find_contact("Ivan"))

    def test_search_contacts_by_name_phone_and_email(self):
        self.book.add_contact(Contact("Ivan", phone="+380501234567", email="ivan@example.com"))
        self.book.add_contact(Contact("Petro", phone="+380671111111", email="petro@example.com"))

        by_name = self.book.search_contacts("ivan")
        by_phone = self.book.search_contacts("067")
        by_email = self.book.search_contacts("petro@")

        self.assertEqual(len(by_name), 1)
        self.assertEqual(by_name[0].name, "Ivan")
        self.assertEqual(len(by_phone), 1)
        self.assertEqual(by_phone[0].name, "Petro")
        self.assertEqual(len(by_email), 1)
        self.assertEqual(by_email[0].name, "Petro")

    def test_get_birthdays_in_days_for_today(self):
        today = date.today().strftime("%Y-%m-%d")
        self.book.add_contact(Contact("BirthdayPerson", phone="+380501234567", birthday=today))

        results = self.book.get_birthdays_in_days(0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "BirthdayPerson")

    def test_days_to_birthday_handles_leap_day(self):
        leap_contact = Contact("Leap", birthday="2000-02-29")
        days = leap_contact.days_to_birthday()

        self.assertIsInstance(days, int)
        self.assertGreaterEqual(days, 0)


if __name__ == "__main__":
    unittest.main()
