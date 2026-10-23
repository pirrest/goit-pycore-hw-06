from collections import UserDict

from .name import Name
from .record import Record


class AddressBook(UserDict):
    """Collection of records keyed by the case-insensitive contact name."""

    def add_record(self, record: Record) -> bool:
        """Add a record to the book.

        Returns:
            True if added, False if a record with the same name already exists.
        """
        key = record.key
        if key in self.data:
            return False
        self.data[key] = record
        return True

    def find(self, name: str) -> Record | None:
        """Return the record with the given name, or None if not found."""
        return self.data.get(Name.to_key(name))

    def delete(self, name: str) -> bool:
        """Delete the record with the given name.

        Returns:
            True if deleted, False if the record was not found.
        """
        key = Name.to_key(name)
        if key not in self.data:
            return False
        del self.data[key]
        return True
