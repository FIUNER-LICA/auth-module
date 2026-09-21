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
        secret_key='test_secret_key',
        locale='en'
    )
    return manager


def test_register_user(auth_manager):
    """Test registering a new user and ensure that the user is created and an email is sent."""
    # Test valid registration
    auth_manager.register_user('test@example.com', 'ValidPass123!')
    user = auth_manager._AuthManager__user_repository.get_user_by_email('test@example.com')

    assert user is not None
    assert user['verified'] is False
    assert len(auth_manager._AuthManager__mail_dispatcher.sent_emails) == 1
    assert auth_manager._AuthManager__mail_dispatcher.sent_emails[0]['to'] == 'test@example.com'

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
    token = auth_manager._AuthManager__token_manager.generate_token({'email': 'test@example.com', 'purpose': 'verification'})

    assert auth_manager.verify_user(token) is True

    user = auth_manager._AuthManager__user_repository.get_user_by_email('test@example.com')
    assert user['verified'] is True

def test_authenticate_user(auth_manager):
    """Test authenticating a user with correct and incorrect credentials."""
    auth_manager.register_user('test@example.com', 'ValidPass123!')

    # Should fail if not verified
    with pytest.raises(ValueError, match='Email is not verified'):
        auth_manager.authenticate_user('test@example.com', 'ValidPass123!')

    # Verify the user
    token = auth_manager._AuthManager__token_manager.generate_token({'email': 'test@example.com', 'purpose': 'verification'})
    auth_manager.verify_user(token)

    # Correct credentials
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
    assert len(auth_manager._AuthManager__mail_dispatcher.sent_emails) == 2
    assert 'Recovery' in auth_manager._AuthManager__mail_dispatcher.sent_emails[1]['subject'] or 'recuperación' in auth_manager._AuthManager__mail_dispatcher.sent_emails[1]['body'].lower()

    # Unregistered email should silently return None to prevent user enumeration
    assert auth_manager.request_password_recovery('nobody@example.com') is None

def test_reset_password(auth_manager):
    """Test resetting a user's password and ensure they can authenticate with the new password."""
    auth_manager.register_user('test@example.com', 'ValidPass123!')

    # Generate a recovery token for the user
    token = auth_manager._AuthManager__token_manager.generate_token({'email': 'test@example.com', 'purpose': 'recovery'})

    # Reset password
    auth_manager.reset_password(token, 'NewValidPass123!')

    # Verify it was updated (we can check by trying to authenticate if it was verified)
    token = auth_manager._AuthManager__token_manager.generate_token({'email': 'test@example.com', 'purpose': 'verification'})
    auth_manager.verify_user(token)

    assert auth_manager.authenticate_user('test@example.com', 'NewValidPass123!') is True

def test_i18n_spanish_backend(tmp_path):
    """Test that setting locale to 'es' results in Spanish error messages and emails."""
    db_file = tmp_path / 'test_users_es.db'
    repo = SQLiteUserRepository(db_path=str(db_file))
    mail = MockMailDispatcher()
    manager = AuthManager(
        mail_dispatcher=mail,
        user_repository=repo,
        base_url='http://localhost:5000',
        secret_key='test_secret_key',
        locale='es'
    )

    # 1. Test duplicate user error in Spanish
    manager.register_user('es@example.com', 'ValidPass123!')
    with pytest.raises(ValueError, match='El usuario ya existe'):
        manager.register_user('es@example.com', 'AnotherPass123!')

    # 2. Test password length error in Spanish
    with pytest.raises(ValueError, match='La contraseña debe tener al menos 8 caracteres'):
        manager.register_user('new@example.com', 'short')

    # 3. Test email sent in Spanish
    assert len(mail.sent_emails) == 1
    assert mail.sent_emails[0]['subject'] == 'Confirma tu cuenta'
    assert 'Por favor confirma tu correo' in mail.sent_emails[0]['body']

def test_i18n_custom_translations(tmp_path):
    """Test that custom translation dictionary overrides work."""
    db_file = tmp_path / 'test_users_custom.db'
    repo = SQLiteUserRepository(db_path=str(db_file))
    mail = MockMailDispatcher()
    custom_translations = {
        'en': {
            'user_exists': 'This email is already registered, try signing in.'
        }
    }
    manager = AuthManager(
        mail_dispatcher=mail,
        user_repository=repo,
        base_url='http://localhost:5000',
        secret_key='test_secret_key',
        locale='en',
        custom_translations=custom_translations
    )

    manager.register_user('custom@example.com', 'ValidPass123!')
    with pytest.raises(ValueError, match='This email is already registered, try signing in.'):
        manager.register_user('custom@example.com', 'AnotherPass123!')

def test_i18n_callable_locale(tmp_path):
    """Test that dynamic locale resolution using a callback works."""
    db_file = tmp_path / 'test_users_dynamic.db'
    repo = SQLiteUserRepository(db_path=str(db_file))
    mail = MockMailDispatcher()

    current_locale = 'en'
    def get_locale():
        return current_locale

    manager = AuthManager(
        mail_dispatcher=mail,
        user_repository=repo,
        base_url='http://localhost:5000',
        secret_key='test_secret_key',
        locale=get_locale
    )

    manager.register_user('dynamic@example.com', 'ValidPass123!')

    # 1. With locale='en', expect English error
    with pytest.raises(ValueError, match='User already exists'):
        manager.register_user('dynamic@example.com', 'AnotherPass123!')

    # 2. Change dynamic locale to 'es', expect Spanish error
    current_locale = 'es'
    with pytest.raises(ValueError, match='El usuario ya existe'):
        manager.register_user('dynamic@example.com', 'AnotherPass123!')

def test_auth_manager_invalid_policy_type(tmp_path):
    """Test that AuthManager raises TypeError if password_policy is not a PasswordPolicy instance."""
    db_file = tmp_path / 'test_users_invalid_policy.db'
    repo = SQLiteUserRepository(db_path=str(db_file))
    mail = MockMailDispatcher()

    with pytest.raises(TypeError, match="password_policy debe ser una instancia de PasswordPolicy, se recibió str"):
        AuthManager(
            mail_dispatcher=mail,
            user_repository=repo,
            base_url='http://localhost:5000',
            secret_key='test_secret_key',
            password_policy="not_a_password_policy_instance"
        )

def test_password_recovery(auth_manager):
    """Test the password recovery and reset token verification flow."""
    manager = auth_manager
    email = 'recover@example.com'

    # 1. User must exist (but now it returns silently)
    assert manager.request_password_recovery(email) is None

    manager.register_user(email, 'Pass1234!')
    manager._AuthManager__user_repository.update_user_verification(email, True)

    # 2. Request recovery (returns None)
    assert manager.request_password_recovery(email) is None

    # 3. Generate token to verify.
    token = manager._AuthManager__token_manager.generate_token({'email': email, 'purpose': 'recovery'})

    # 4. Verify valid token
    assert manager.verify_password_reset_token(token) == email

    # 5. Reset password to mark token as used
    manager.reset_password(token, 'NewPass1234!')

    # 6. Verify token is now invalid (used)
    assert manager.verify_password_reset_token(token) is None

    # 6. Verify invalid token
    assert manager.verify_password_reset_token('invalid_token_string') is None

def test_oauth_user_creation(auth_manager):
    """Test getting or creating an OAuth user."""
    manager = auth_manager
    email = 'oauth@example.com'

    # 1. Create new user
    user = manager.get_or_create_oauth_user(email, name='OAuth User', provider='google')
    assert user['email'] == email
    assert user['name'] == 'OAuth User'
    assert user['verified'] is True

    # 2. Get existing user
    user_existing = manager.get_or_create_oauth_user(email, provider='google')
    assert user_existing['email'] == email
    assert user_existing['name'] == 'OAuth User'
