"""Length constraint rule."""

from dataclasses import dataclass

from .base import PasswordRule


@dataclass
class LengthPasswordRule(PasswordRule):
    """Validates that a password meets the minimum length."""
    value: int = 8
    message: str = 'Password must be at least {value} characters long.'

    def validate(self, password: str) -> tuple[bool, str]:
        if len(password) < self.value:
            return False, self.message.format(value=self.value)
        return True, ''
