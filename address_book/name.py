from .field import Field


class Name(Field):
    """Required contact name.

    Raises:
        TypeError: If the name is not a string.
        ValueError: If the name is empty after stripping whitespace.
    """

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Name must be a string, got {type(value).__name__}")
        if not value.strip():
            raise ValueError("Name must not be empty")
        super().__init__(value)

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
