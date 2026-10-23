import re

from .field import Field


class Phone(Field):
    """Contact phone number, expected to consist of exactly 10 digits.

    The constructor does not validate the value, call `is_valid` to check it.
    """

    COUNTRY_CODE = "+38"

    @property
    def is_required(self) -> bool:
        return False

    @staticmethod
    def normalize_phone(phone_number: str) -> str | None:
        """Normalize a phone number to the '+<digits>' format.

        All characters except digits and a leading '+' are removed. A number that
        already has a '+' keeps its country code, one starting with '380' gets only
        the '+', any other number gets the default '+38' prefix.

        Args:
            phone_number: Phone number in an arbitrary format.

        Returns:
            Normalized number, or None if the input is not a string or has no digits.
        """
        if not isinstance(phone_number, str):
            return None
        digits = re.sub(r"\D", "", phone_number)
        if not digits:
            return None
        if re.match(r"\s*\+", phone_number):
            return f"+{digits}"
        if digits.startswith(Phone.COUNTRY_CODE.lstrip("+") + "0"):
            return f"+{digits}"
        return f"{Phone.COUNTRY_CODE}{digits}"

    @staticmethod
    def to_key(phone_number: str) -> str:
        """Return the key used to compare phone numbers.

        It is the normalized number, or the raw value if it cannot be normalized.
        """
        normalized = Phone.normalize_phone(phone_number)
        return phone_number if normalized is None else normalized

    @property
    def key(self) -> str:
        """Key identifying this phone within a record."""
        return Phone.to_key(self.value)

    @property
    def is_valid(self) -> bool:
        """Return True if the value is a string of exactly 10 ASCII digits."""
        return isinstance(self.value, str) and re.fullmatch(r"[0-9]{10}", self.value) is not None
