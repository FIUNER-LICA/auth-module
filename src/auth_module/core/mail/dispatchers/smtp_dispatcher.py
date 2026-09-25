"""
Implementation of the email dispatcher using the 'sender' library.
"""

from sender import Mail, Message

from ..config import AbsEmailServerConfig
from .base import MailDispatcher


class SmtpMailDispatcher(MailDispatcher):
    """
    Email dispatcher implementation using the 'sender' SMTP library.
    """

    def __init__(self):
        self._mail = None

    def initialize(self, config: AbsEmailServerConfig) -> None:
        """
        Initializes the SMTP connection parameters using the provided configuration.

        Args:
            config (AbsEmailServerConfig): The email server configuration.
        """
        smtp_host = config.mail_server
        smtp_port = config.mail_port
        smtp_user = config.mail_username
        smtp_pass = config.mail_password
        smtp_address = config.mail_sender_address
        name_sender = config.name_sender

        from_addr = (name_sender, smtp_address)
        mail_use_tls = config.mail_use_tls

        self._mail = Mail(
            host=smtp_host,
            port=smtp_port,
            username=smtp_user,
            password=smtp_pass,
            fromaddr=from_addr,
            use_tls=mail_use_tls
        )

    def send(self, to_email: str, subject: str, body: str) -> None:
        """
        Sends an email.

        Args:
            to_email (str): Recipient email address.
            subject (str): Email subject.
            body (str): Email body (HTML).
        """
        if not self._mail:
            raise RuntimeError('SmtpMailDispatcher has not been initialized.')

        html = body
        msg = Message(subject=subject, to=to_email, html=html)

        self._mail.send(msg)
