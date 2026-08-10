"""
Console email dispatcher for development and testing.
"""

from .base import MailDispatcher


class ConsoleMailDispatcher(MailDispatcher):
    """
    A dummy email dispatcher that prints emails to the console instead of sending them.
    Useful for local development and testing.
    """

    def send(self, to_email: str, subject: str, body: str, logo_image_file: str | None = None) -> bool:
        """
        Prints the email details to standard output.
        """
        print('-' * 40)
        print('--- MOCK EMAIL INTERCEPTED ---')
        print(f'To: {to_email}')
        print(f'Subject: {subject}')
        print(f'Body Snippet: {body[:150]}...')
        if logo_image_file:
            print(f'Attachment: {logo_image_file}')
        print('-' * 40)
        return True
