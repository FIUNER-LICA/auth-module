"""
Password hashing, validation, and policy enforcement utilities.
"""

import re

from werkzeug.security import generate_password_hash, check_password_hash


class PasswordPolicy:
    """
    Configuration for password strength requirements.
    """

    def __init__(self, min_length: int = 8, regex_pattern: str | None = None):
        """
        Initializes the password policy.

        Args:
            min_length (int): Minimum required length for the password. Defaults to 8.
            regex_pattern (str | None): Optional regex pattern the password must match.
        """
        self.min_length = min_length
        self.regex_pattern = regex_pattern

    def validate(self, password: str) -> tuple[bool, str]:
        """
        Validates a password against the defined policy.

        Args:
            password (str): The password to check.

        Returns:
            tuple[bool, str]: A boolean indicating success, and an error message if failed.
        """
        if len(password) < self.min_length:
            return False, f'Password must be at least {self.min_length} characters long.'

        if self.regex_pattern:
            if not re.match(self.regex_pattern, password):
                return False, 'Password does not meet the complexity requirements.'

        return True, 'Password is valid.'


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

def hash_password(password: str) -> str:
    """
    Hashes a password using a secure algorithm.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return generate_password_hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies a plain text password against a hashed one.

    Args:
        password (str): The plain text password.
        hashed (str): The previously hashed password.

    Returns:
        bool: True if they match, False otherwise.
    """
    return check_password_hash(hashed, password)
