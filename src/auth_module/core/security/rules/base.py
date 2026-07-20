"""Abstract base classes for password rules."""
from abc import ABC, abstractmethod


class AbsPasswordRule(ABC):
    """Abstract base class for all password validation rules."""

    @abstractmethod
    def validate(self, password: str) -> tuple[bool, str]:
        """
        Validates the password against this specific rule.

        Args:
            password (str): The password to check.

        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
