"""
Unit tests for the SMTP Mail Dispatcher and its config.
"""

from unittest.mock import patch

import pytest

from auth_module.core.mail.config import EmailEnvConfig
from auth_module.core.mail.dispatchers import SmtpMailDispatcher


def test_email_env_config(monkeypatch):
    """Test loading email configuration from environment variables."""
    monkeypatch.setenv('MAIL_SERVER', 'smtp.test.com')
    monkeypatch.setenv('MAIL_PORT', '465')
    monkeypatch.setenv('MAIL_USERNAME', 'test_user')
    monkeypatch.setenv('MAIL_PASSWORD', 'test_pass')
    monkeypatch.setenv('MAIL_USE_TLS', 'False')
    monkeypatch.setenv('MAIL_USE_SSL', 'True')
    monkeypatch.setenv('MAIL_DEFAULT_SENDER', 'no-reply@test.com')
    monkeypatch.setenv('MAIL_SENDER_ADDRESS', 'sender@test.com')
    monkeypatch.setenv('NAME_SENDER', 'Test Sender')

    config = EmailEnvConfig()

    assert config.mail_server == 'smtp.test.com'
    assert config.mail_port == 465
    assert config.mail_username == 'test_user'
    assert config.mail_password == 'test_pass'
    assert config.mail_use_tls is False
    assert config.mail_sender_address == 'sender@test.com'
    assert config.name_sender == 'Test Sender'

@patch('auth_module.core.mail.dispatchers.smtp_dispatcher.Mail')
def test_smtp_mail_dispatcher_success(mock_mail_class, monkeypatch):
    """Test successful email dispatch using SmtpMailDispatcher."""
    # Set required env vars to avoid validation errors
    monkeypatch.setenv('MAIL_SERVER', 'smtp.test.com')
    monkeypatch.setenv('MAIL_PORT', '465')
    monkeypatch.setenv('MAIL_USERNAME', 'test_user')
    monkeypatch.setenv('MAIL_PASSWORD', 'test_pass')
    monkeypatch.setenv('MAIL_SENDER_ADDRESS', 'sender@test.com')
    monkeypatch.setenv('NAME_SENDER', 'Test Sender')

    config = EmailEnvConfig()
    dispatcher = SmtpMailDispatcher()
    dispatcher.initialize(config)

    # Send email
    result = dispatcher.send('recipient@test.com', 'Test Subject', 'Test Body')

    # Send should succeed, but note that the send method of dispatcher doesn't return anything. It just executes.
    # We should assert that we don't get an exception, and that the inner mock was called.
    assert result is None
    mock_mail_instance = mock_mail_class.return_value
    mock_mail_instance.send.assert_called_once()

@patch('auth_module.core.mail.dispatchers.smtp_dispatcher.Mail')
def test_smtp_mail_dispatcher_failure(mock_mail_class, monkeypatch):
    """Test failure in email dispatch using SmtpMailDispatcher."""
    monkeypatch.setenv('MAIL_SERVER', 'smtp.test.com')
    monkeypatch.setenv('MAIL_PORT', '465')
    monkeypatch.setenv('MAIL_USERNAME', 'test_user')
    monkeypatch.setenv('MAIL_PASSWORD', 'test_pass')
    monkeypatch.setenv('MAIL_SENDER_ADDRESS', 'sender@test.com')
    monkeypatch.setenv('NAME_SENDER', 'Test Sender')

    config = EmailEnvConfig()
    dispatcher = SmtpMailDispatcher()
    dispatcher.initialize(config)

    # Make the send method raise an exception
    mock_mail_instance = mock_mail_class.return_value
    mock_mail_instance.send.side_effect = Exception('SMTP Connection Failed')

    with pytest.raises(Exception, match='SMTP Connection Failed'):
        dispatcher.send('recipient@test.com', 'Test Subject', 'Test Body')
