from .field import Field


class Name(Field):
    """Required contact name."""

    @property
    def is_required(self) -> bool:
        return True

    @staticmethod
    def to_key(name: str) -> str:
        """Return the case- and surrounding-whitespace-insensitive key for a name."""
        return name.strip().casefold()

    @property
    def key(self) -> str:
        """Key identifying this name in an address book."""
        return Name.to_key(self.value)

    @property
    def is_valid(self) -> bool:
        """Return True if the name is not empty after stripping whitespace."""
        return isinstance(self.value, str) and bool(self.value.strip())
