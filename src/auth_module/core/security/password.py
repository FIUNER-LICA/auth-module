"""
Password hashing, validation, and policy enforcement utilities.
"""

from dataclasses import dataclass, field

from .rules import AbsPasswordRule, LengthRule, RegexRule


@dataclass
class PasswordPolicyConfig:
    """
    Configuration data structure for password strength requirements.
    Rules and their error messages are grouped together dynamically.
    """
    rules: list[AbsPasswordRule] = field(default_factory=lambda: [LengthRule(), RegexRule()])
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
        for rule in self.config.rules:
            is_valid, msg = rule.validate(password)
            if not is_valid:
                return False, msg

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
