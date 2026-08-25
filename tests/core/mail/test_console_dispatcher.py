"""
Unit tests for the ConsoleMailDispatcher.
"""

from auth_module.core.mail.console_dispatcher import ConsoleMailDispatcher


def test_console_mail_dispatcher(capsys):
    """Test that the ConsoleMailDispatcher correctly prints to stdout."""
    dispatcher = ConsoleMailDispatcher()

    # Send a test email via the console dispatcher
    result = dispatcher.send(
        to_email='test@example.com',
        subject='Test Subject',
        body='This is a test body.'
    )

    # Must return always None
    assert result is None

    # Check the captured output
    captured = capsys.readouterr()

    assert '--- [CONSOLE MAIL DISPATCHER] ---' in captured.out
    assert 'To: test@example.com' in captured.out
    assert 'Subject: Test Subject' in captured.out
    assert 'This is a test body.' in captured.out
