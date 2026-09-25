"""
Console email dispatcher for development and testing.
"""

from .base import MailDispatcher


class ConsoleMailDispatcher(MailDispatcher):
    """
    A dummy email dispatcher that prints emails to the console instead of sending them.
    Useful for local development and testing.
    """

    def send(self, to_email: str, subject: str, body: str) -> None:
        """
        Simulates sending an email by printing to the console.

        Args:
            to_email (str): Recipient email address.
            subject (str): Email subject.
            body (str): Email body.
        """
        print('--- [CONSOLE MAIL DISPATCHER] ---')
        print(f'To: {to_email}')
        print(f'Subject: {subject}')
        print('Body:')
        print(body)
        print('---------------------------------')
