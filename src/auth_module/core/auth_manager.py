"""
Authentication manager that encapsulates user registration, login, and recovery logic.
"""

from .db.repository import UserRepository
from .mail.base import MailDispatcher
from .security.hasher import PasswordHasher, WerkzeugPasswordHasher
from .security.password import PasswordPolicy
from .tokens import TokenManager


class AuthManager:
    """
    Core authentication manager handling framework-agnostic business logic.
    """

    def __init__(
        self,
        secret_key: str,
        mail_dispatcher: MailDispatcher,
        user_repository: UserRepository,
        base_url: str,
        password_policy: PasswordPolicy | None = None,
        password_hasher: PasswordHasher | None = None
    ):
        """
        Initializes the AuthManager.

        Args:
            secret_key (str): Secret key for token generation.
            mail_dispatcher (MailDispatcher): The email sending service.
            user_repository (UserRepository): The user database repository.
            base_url (str): The base URL of the application for email links.
            password_policy (PasswordPolicy | None): Custom password requirements.
            password_hasher (PasswordHasher | None): Custom password hashing mechanism. Defaults to Werkzeug.
        """
        if not base_url:
            raise ValueError('A base_url must be provided for generating absolute links.')

        self.token_manager = TokenManager(secret_key)
        self.mail_dispatcher = mail_dispatcher
        self.user_repository = user_repository
        self.base_url = base_url.rstrip('/')
        self.password_policy = password_policy or PasswordPolicy()
        self.password_hasher = password_hasher or WerkzeugPasswordHasher()

        # Simulating state for used tokens (could also be moved to the DB)
        self.used_pw_reset_tokens = set()

    def register_user(self, email: str, password: str) -> bool:
        """
        Registers a new user and sends a verification email.

        Args:
            email (str): The user's email.
            password (str): The user's plain text password.

        Returns:
            bool: True if registration is successful.

        Raises:
            ValueError: If the user already exists or the password doesn't meet the policy.
        """
        if self.user_repository.get_user_by_email(email):
            raise ValueError('User already exists')

        is_valid_pwd, pwd_msg = self.password_policy.validate(password)
        if not is_valid_pwd:
            raise ValueError(pwd_msg)

        pwd_hash = self.password_hasher.hash(password)
        self.user_repository.create_user(email=email, password_hash=pwd_hash, verified=False)

        token = self.token_manager.generate_token(email)
        verify_url = f'{self.base_url}/verify/{token}'

        self.mail_dispatcher.send(
            to_email=email,
            subject='Confirm your account',
            body=f'Please confirm your email by clicking here: {verify_url}'
        )
        return True

    def reset_password(self, email: str, password: str) -> bool:
        """
        Resets the password for an existing user.

        Args:
            email (str): The user's email.
            password (str): The new plain text password.

        Returns:
            bool: True if password reset was successful.

        Raises:
            ValueError: If the user does not exist or password is invalid.
        """
        if not self.user_repository.get_user_by_email(email):
            raise ValueError('User does not exist')

        is_valid_pwd, pwd_msg = self.password_policy.validate(password)
        if not is_valid_pwd:
            raise ValueError(pwd_msg)

        pwd_hash = self.password_hasher.hash(password)
        self.user_repository.update_user_password(email, pwd_hash)
        return True

    def verify_user(self, token: str) -> bool:
        """
        Verifies a user's email using the provided token.

        Args:
            token (str): The verification token.

        Returns:
            bool: True if successful, False otherwise.
        """
        email = self.token_manager.confirm_token(token)
        if not email:
            return False

        user = self.user_repository.get_user_by_email(email)
        if not user:
            return False

        self.user_repository.update_user_verification(email, True)
        return True

    def verify_password_reset_token(self, token: str) -> str | None:
        """
        Verifies if the password reset token is valid and hasn't expired or been used.

        Args:
            token (str): The password reset token.

        Returns:
            str | None: The associated email if valid, None otherwise.
        """
        email = self.token_manager.confirm_token(token)

        user = self.user_repository.get_user_by_email(email) if email else None

        if token in self.used_pw_reset_tokens and user:
            return None

        self.used_pw_reset_tokens.add(token)

        if token in self.used_pw_reset_tokens and not user:
            self.used_pw_reset_tokens.remove(token)

        if not user:
            return None

        return email

    def authenticate_user(self, email: str, password: str) -> bool:
        """
        Authenticates a user using email and password.

        Args:
            email (str): The user's email.
            password (str): The user's plain text password.

        Returns:
            bool: True if authentication is successful, False otherwise.

        Raises:
            ValueError: If the user's email is not verified.
        """
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return False

        if not user.get('verified'):
            raise ValueError('Email is not verified')

        return user.get('password') and self.password_hasher.verify(password, user['password'])

    def get_or_create_oauth_user(self, email: str, name: str | None = None, provider: str | None = None) -> dict[str, any]:
        """
        Gets a user or creates a new one marked as verified if they come from an OAuth provider.

        Args:
            email (str): The user's email.
            name (str | None): The user's name.
            provider (str | None): The OAuth provider name (e.g., 'google').

        Returns:
            dict[str, any]: The user's data dictionary.
        """
        user = self.user_repository.get_user_by_email(email)
        if user:
            return user

        self.user_repository.create_user(
            email=email,
            password_hash=None,
            verified=True,
            name=name,
            oauth_provider=provider
        )
        return self.user_repository.get_user_by_email(email)

    def request_password_recovery(self, email: str) -> bool:
        """
        Initiates a password recovery process and sends a recovery email.

        Args:
            email (str): The user's email.

        Returns:
            bool: True if the email was successfully sent.

        Raises:
            ValueError: If the user does not exist.
        """
        if not self.user_repository.get_user_by_email(email):
            raise ValueError('No user exists with that email')

        token = self.token_manager.generate_token(email)
        recovery_url = f'{self.base_url}/reset-password/{token}'

        self.mail_dispatcher.send(
            to_email=email,
            subject='Password Recovery',
            body=f'To reset your password, please click here: {recovery_url}'
        )
        return True
