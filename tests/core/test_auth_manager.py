"""
Unit tests for AuthManager.
"""
import pytest

from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.base import MailDispatcher


class MockMailDispatcher(MailDispatcher):
    """A mock mail dispatcher for testing purposes."""

    def __init__(self):
        self.sent_emails = []

    def send(self, to_email: str, subject: str, body: str, logo_image_file: str | None = None) -> bool:
        self.sent_emails.append({'to': to_email, 'subject': subject, 'body': body})
        return True


@pytest.fixture
def auth_manager(tmp_path):
    """Fixture to initialize an AuthManager with a temporary SQLite database and a mock mail dispatcher."""
    db_file = tmp_path / 'test_users.db'
    repo = SQLiteUserRepository(db_path=str(db_file))
    mail = MockMailDispatcher()
    manager = AuthManager(
        mail_dispatcher=mail,
        user_repository=repo,
        base_url='http://localhost:5000',
        secret_key='test_secret_key'
    )
    return manager


def test_register_user(auth_manager):
    """Test registering a new user and ensure that the user is created and an email is sent."""
    # Test valid registration
    auth_manager.register_user('test@example.com', 'ValidPass123!')
    user = auth_manager.user_repository.get_user_by_email('test@example.com')

    assert user is not None
    assert user['verified'] is False
    assert len(auth_manager.mail_dispatcher.sent_emails) == 1
    assert auth_manager.mail_dispatcher.sent_emails[0]['to'] == 'test@example.com'

def test_register_user_invalid_password(auth_manager):
    """Test registering a user with an invalid password (too short)."""
    with pytest.raises(ValueError, match='must be at least 8 characters'):
        auth_manager.register_user('test@example.com', 'short')

def test_register_duplicate_user(auth_manager):
    """Test that registering a user with an email that already exists raises an error."""
    auth_manager.register_user('test@example.com', 'ValidPass123!')
    with pytest.raises(ValueError, match='already exists'):
        auth_manager.register_user('test@example.com', 'AnotherPass123!')

def test_verify_user(auth_manager):
    """Test verifying a user using a valid token."""
    auth_manager.register_user('test@example.com', 'ValidPass123!')

    # We need to manually generate a token for testing or extract it from the email body
    # Let's just generate one using the internal token manager
    token = auth_manager.token_manager.generate_token('test@example.com')

    assert auth_manager.verify_user(token) is True

    user = auth_manager.user_repository.get_user_by_email('test@example.com')
    assert user['verified'] is True

def test_authenticate_user(auth_manager):
    """Test authenticating a user with correct and incorrect credentials."""
    auth_manager.register_user('test@example.com', 'ValidPass123!')

    # Should fail if not verified
    with pytest.raises(ValueError, match='Email is not verified'):
        auth_manager.authenticate_user('test@example.com', 'ValidPass123!')

    # Verify the user
    token = auth_manager.token_manager.generate_token('test@example.com')
    auth_manager.verify_user(token)

    # Should succeed now
    assert auth_manager.authenticate_user('test@example.com', 'ValidPass123!') is True

    # Wrong password
    assert auth_manager.authenticate_user('test@example.com', 'WrongPass123!') is False

    # Non-existent user
    assert auth_manager.authenticate_user('nobody@example.com', 'ValidPass123!') is False

def test_request_password_recovery(auth_manager):
    """Test requesting password recovery for a registered user and ensure an email is sent."""
    auth_manager.register_user('test@example.com', 'ValidPass123!')

    auth_manager.request_password_recovery('test@example.com')

    # 2 emails sent: 1 for registration, 1 for recovery
    assert len(auth_manager.mail_dispatcher.sent_emails) == 2
    assert "Recovery" in auth_manager.mail_dispatcher.sent_emails[1]['subject'] or 'recuperación' in auth_manager.mail_dispatcher.sent_emails[1]['body'].lower()

    # Unregistered email should silently fail or log, but currently it raises ValueError
    with pytest.raises(ValueError, match='No user exists'):
        auth_manager.request_password_recovery('nobody@example.com')

def test_reset_password(auth_manager):
    """Test resetting a user's password and ensure they can authenticate with the new password."""
    auth_manager.register_user('test@example.com', 'ValidPass123!')

    # Reset password
    auth_manager.reset_password('test@example.com', 'NewValidPass123!')

    # Verify it was updated (we can check by trying to authenticate if it was verified)
    token = auth_manager.token_manager.generate_token('test@example.com')
    auth_manager.verify_user(token)

    assert auth_manager.authenticate_user('test@example.com', 'NewValidPass123!') is True
