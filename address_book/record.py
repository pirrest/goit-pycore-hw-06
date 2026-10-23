from .name import Name
from .phone import Phone


class Record:
    """Contact record with a name and a list of phones."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    @property
    def key(self) -> str:
        """Key identifying this record in an address book."""
        return self.name.key

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def _index_of_phone(self, phone_number: str) -> int | None:
        """Return the index of the phone matching the given number, or None."""
        key = Phone.to_key(phone_number)
        for index, phone in enumerate(self.phones):
            if phone.key == key:
                return index
        return None

    def add_phone(self, phone_number: str) -> bool:
        """Add a phone to the record.

        Validity of the number is not checked yet.

        Returns:
            True if added, False if the record already has this phone.
        """
        if self._index_of_phone(phone_number) is not None:
            return False
        self.phones.append(Phone(phone_number))
        return True

    def remove_phone(self, phone_number: str) -> bool:
        """Remove a phone from the record.

        Returns:
            True if removed, False if the phone was not found.
        """
        index = self._index_of_phone(phone_number)
        if index is None:
            return False
        del self.phones[index]
        return True

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> bool:
        """Replace a phone in place, keeping its position in the list.

        Validity of the new number is not checked yet.

        Returns:
            True if replaced, False if the old phone was not found or the new
            number is already present in the record as another phone.
        """
        index = self._index_of_phone(old_phone_number)
        if index is None:
            return False
        new_key = Phone.to_key(new_phone_number)
        for other_index, phone in enumerate(self.phones):
            if other_index != index and phone.key == new_key:
                return False
        self.phones[index] = Phone(new_phone_number)
        return True

    def find_phone(self, phone_number: str) -> Phone | None:
        """Return the phone matching the given number, or None if not found."""
        index = self._index_of_phone(phone_number)
        return None if index is None else self.phones[index]
