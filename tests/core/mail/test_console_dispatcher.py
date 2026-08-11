"""
Unit tests for the ConsoleMailDispatcher.
"""

from auth_module.core.mail.console_dispatcher import ConsoleMailDispatcher


def test_console_mail_dispatcher(capsys):
    """Test that the ConsoleMailDispatcher correctly prints to stdout."""
    dispatcher = ConsoleMailDispatcher()

    # Enviar un mail por consola
    result = dispatcher.send(
        to_email='test@example.com',
        subject='Test Subject',
        body='This is a test body.'
    )

    # Debe retornar True siempre
    assert result is True

    # Capturar la salida de consola
    captured = capsys.readouterr()

    assert 'To: test@example.com' in captured.out
    assert 'Subject: Test Subject' in captured.out
    assert 'This is a test body.' in captured.out
