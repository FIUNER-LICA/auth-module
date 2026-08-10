"""Regex constraint rule."""

import re
from dataclasses import dataclass

from .base import AbsPasswordRule


@dataclass
class RegexRule(AbsPasswordRule):
    """Validates that a password matches a regex pattern."""
    pattern: str | None = None
    message: str = 'Password does not meet the complexity requirements.'

    def validate(self, password: str) -> tuple[bool, str]:
        if self.pattern and not re.match(self.pattern, password):
            return False, self.message
        return True, ''
