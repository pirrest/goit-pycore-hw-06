import unittest

from address_book import AddressBook, Field, Name, Phone, Record


class FieldValidationTests(unittest.TestCase):
    def test_phone_valid(self):
        self.assertEqual(Phone("1234567890").value, "1234567890")

    def test_phone_invalid_raises_value_error(self):
        for value in ("123456789", "12345678901", "12345abcde", "", "123-456-7890", "١٢٣٤٥٦٧٨٩٠"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Phone(value)

    def test_phone_not_a_string_raises_type_error(self):
        for value in (1234567890, None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    Phone(value)

    def test_name_valid_keeps_original_value(self):
        self.assertEqual(Name(" John ").value, " John ")

    def test_name_empty_after_strip_raises_value_error(self):
        for value in ("", "   ", "\t\n"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Name(value)

    def test_name_not_a_string_raises_type_error(self):
        for value in (None, 123):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    Name(value)

    def test_record_with_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            Record("  ")


class RequiredTests(unittest.TestCase):
    def test_field_is_optional_by_default(self):
        self.assertFalse(Field("x").is_required)

    def test_phone_is_optional(self):
        self.assertFalse(Phone("1234567890").is_required)

    def test_name_is_required(self):
        self.assertTrue(Name("John").is_required)


class KeyTests(unittest.TestCase):
    def test_name_to_key(self):
        self.assertEqual(Name.to_key("  JoHn "), "john")

    def test_name_key(self):
        self.assertEqual(Name(" John").key, "john")

    def test_phone_to_key_is_normalized(self):
        self.assertEqual(Phone.to_key("(050) 123-45-67"), "+380501234567")

    def test_phone_to_key_falls_back_to_raw_value(self):
        self.assertEqual(Phone.to_key("abc"), "abc")

    def test_phone_key(self):
        self.assertEqual(Phone("0501234567").key, "+380501234567")

    def test_record_key(self):
        self.assertEqual(Record("  JANE").key, "jane")


class NormalizePhoneTests(unittest.TestCase):
    def test_formats(self):
        cases = {
            "067\t123 4567": "+380671234567",
            "(095) 234-5678\n": "+380952345678",
            "+380 44 123 4567": "+380441234567",
            "380501234567": "+380501234567",
            "    +38(050)123-32-34": "+380501233234",
            "+49 151 2345 6789": "+4915123456789",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(Phone.normalize_phone(raw), expected)

    def test_no_digits_or_not_a_string(self):
        self.assertIsNone(Phone.normalize_phone("abc"))
        self.assertIsNone(Phone.normalize_phone(None))


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")

    def test_add_phone(self):
        self.assertTrue(self.record.add_phone("9876543210"))
        self.assertEqual(len(self.record.phones), 3)

    def test_add_duplicate_phone_returns_false(self):
        self.assertFalse(self.record.add_phone("1234567890"))
        self.assertEqual(len(self.record.phones), 2)

    def test_add_duplicate_in_other_format_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.record.add_phone("(123) 456-7890")
        self.assertEqual(len(self.record.phones), 2)

    def test_add_invalid_phone_raises_and_keeps_record(self):
        for value in ("123", "abc"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.record.add_phone(value)
        with self.assertRaises(TypeError):
            self.record.add_phone(1234567890)
        self.assertEqual(len(self.record.phones), 2)

    def test_edit_to_invalid_phone_raises_and_keeps_record(self):
        with self.assertRaises(ValueError):
            self.record.edit_phone("1234567890", "123")
        with self.assertRaises(ValueError):
            self.record.edit_phone("0000000000", "123")
        self.assertEqual([p.value for p in self.record.phones], ["1234567890", "5555555555"])

    def test_remove_phone(self):
        self.assertTrue(self.record.remove_phone("1234567890"))
        self.assertEqual([p.value for p in self.record.phones], ["5555555555"])

    def test_remove_missing_phone_returns_false(self):
        self.assertFalse(self.record.remove_phone("0000000000"))
        self.assertEqual(len(self.record.phones), 2)

    def test_edit_phone_keeps_position(self):
        self.assertTrue(self.record.edit_phone("1234567890", "1112223333"))
        self.assertEqual([p.value for p in self.record.phones], ["1112223333", "5555555555"])

    def test_edit_missing_phone_returns_false(self):
        self.assertFalse(self.record.edit_phone("0000000000", "1112223333"))

    def test_edit_to_existing_phone_returns_false(self):
        self.assertFalse(self.record.edit_phone("1234567890", "5555555555"))
        self.assertEqual([p.value for p in self.record.phones], ["1234567890", "5555555555"])

    def test_edit_phone_to_itself(self):
        self.assertTrue(self.record.edit_phone("1234567890", "1234567890"))
        self.assertEqual(len(self.record.phones), 2)

    def test_find_phone(self):
        found = self.record.find_phone("5555555555")
        self.assertIsNotNone(found)
        self.assertEqual(str(found), "5555555555")

    def test_find_phone_normalized(self):
        self.assertIsNotNone(self.record.find_phone("555-555-5555"))

    def test_find_missing_phone_returns_none(self):
        self.assertIsNone(self.record.find_phone("0000000000"))

    def test_lookup_with_non_normalizable_value_finds_nothing(self):
        self.assertIsNone(self.record.find_phone("abc"))
        self.assertFalse(self.record.remove_phone("abc"))
        self.assertFalse(self.record.edit_phone("abc", "1112223333"))
        self.assertEqual(len(self.record.phones), 2)

    def test_str(self):
        self.assertEqual(str(self.record), "Contact name: John, phones: 1234567890; 5555555555")


class AddressBookTests(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        self.john = Record("John")
        self.book.add_record(self.john)

    def test_add_and_find(self):
        self.assertIs(self.book.find("John"), self.john)

    def test_find_is_case_insensitive(self):
        self.assertIs(self.book.find("jOHN"), self.john)

    def test_key_is_normalized_and_name_keeps_original(self):
        self.assertIn("john", self.book.data)
        self.assertEqual(self.john.name.value, "John")

    def test_key_ignores_surrounding_whitespace(self):
        self.assertIs(self.book.find("  John "), self.john)
        self.assertFalse(self.book.add_record(Record(" john ")))
        self.assertTrue(self.book.delete(" JOHN  "))

    def test_find_missing_returns_none(self):
        self.assertIsNone(self.book.find("Nobody"))

    def test_add_duplicate_name_returns_false_without_overwrite(self):
        self.assertFalse(self.book.add_record(Record("JOHN")))
        self.assertIs(self.book.find("John"), self.john)
        self.assertEqual(len(self.book.data), 1)

    def test_add_returns_true(self):
        self.assertTrue(self.book.add_record(Record("Jane")))

    def test_delete(self):
        self.assertTrue(self.book.delete("john"))
        self.assertIsNone(self.book.find("John"))

    def test_delete_missing_returns_false(self):
        self.assertFalse(self.book.delete("Nobody"))


class DemoScenarioTests(unittest.TestCase):
    def test_task_scenario(self):
        book = AddressBook()
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        book.add_record(john_record)
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)

        john = book.find("John")
        john.edit_phone("1234567890", "1112223333")
        self.assertEqual(str(john), "Contact name: John, phones: 1112223333; 5555555555")
        self.assertEqual(f"{john.name}: {john.find_phone('5555555555')}", "John: 5555555555")

        book.delete("Jane")
        self.assertIsNone(book.find("Jane"))


if __name__ == "__main__":
    unittest.main()
