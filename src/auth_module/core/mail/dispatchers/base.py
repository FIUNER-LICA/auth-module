"""
Abstract base classes for email dispatch.
"""

from abc import ABC, abstractmethod


class MailDispatcher(ABC):
    """Abstract base class for email dispatchers."""

    @abstractmethod
    def send(self, to_email: str, subject: str, body: str) -> None:
        """
        Sends an email.

        Args:
            to_email (str): Recipient email address.
            subject (str): Email subject.
            body (str): Email body (HTML or plain text).
        """
