"""
Password hashing, validation, and policy enforcement utilities.
"""

from dataclasses import dataclass, field
import re


@dataclass
class LengthRule:
    """Configuration for minimum password length."""
    value: int = 8
    message: str = 'Password must be at least {value} characters long.'

@dataclass
class RegexRule:
    """Configuration for password regex constraints."""
    pattern: str | None = None
    message: str = 'Password does not meet the complexity requirements.'

@dataclass
class PasswordPolicyConfig:
    """
    Configuration data structure for password strength requirements.
    Rules and their error messages are grouped together.
    """
    length: LengthRule = field(default_factory=LengthRule)
    regex: RegexRule = field(default_factory=RegexRule)
    msg_valid: str = 'Password is valid.'


class PasswordPolicy:
    """Configuration for password strength requirements using a customizable config."""

    def __init__(self, config: PasswordPolicyConfig | None = None):
        """
        Initializes the password policy with the given configuration.

        Args:
            config (PasswordPolicyConfig | None): Configuration and customized messages.
        """
        self.config = config or PasswordPolicyConfig()

    def validate(self, password: str) -> tuple[bool, str]:
        """
        Validates a password against the defined policy.

        Args:
            password (str): The password to check.

        Returns:
            tuple[bool, str]: A boolean indicating success, and an error message if failed.
        """
        if len(password) < self.config.length.value:
            return False, self.config.length.message.format(value=self.config.length.value)

        if self.config.regex.pattern:
            if not re.match(self.config.regex.pattern, password):
                return False, self.config.regex.message

        return True, self.config.msg_valid


def is_password_valid(password: str, repassword: str) -> bool:
    """
    Checks if two passwords match.

    Args:
        password (str): The primary password.
        repassword (str): The confirmation password.

    Returns:
        bool: True if they match, False otherwise.
    """
    return password == repassword
