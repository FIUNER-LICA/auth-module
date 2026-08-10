"""
Token generation and validation using itsdangerous.
"""

import hashlib
import hmac

from itsdangerous import URLSafeTimedSerializer


class TokenManager:
    """
    Manages the creation and validation of secure, timed tokens.
    """

    def __init__(self, secret_key: str, salt: str | None = None) -> None:
        """
        Initializes the TokenManager.

        Args:
            secret_key (str): The secret key used to sign the tokens.
            salt (str | None): The salt used to namespace the tokens.
        """
        if not secret_key:
            raise ValueError('A secret_key is required for token generation.')

        self.secret_key = secret_key

        if salt is None:
            self.salt = hmac.new(
                secret_key.encode('utf-8'),
                msg=b'auth_module_secure_salt_derivation',
                digestmod=hashlib.sha256
            ).hexdigest()
        else:
            self.salt = salt

        self.serializer = URLSafeTimedSerializer(self.secret_key)

    def generate_token(self, data: str) -> str:
        """
        Generates a secure token for the provided data (e.g., an email address).

        Args:
            data (str): The data to encode in the token.

        Returns:
            str: The generated token.
        """
        return self.serializer.dumps(data, salt=self.salt)

    def confirm_token(self, token: str, expiration_seconds: int = 3600) -> str | None:
        """
        Confirms the validity of a token and extracts the embedded data.

        Args:
            token (str): The token to verify.
            expiration_seconds (int): Maximum age of the token in seconds.

        Returns:
            str | None: The extracted data if valid and not expired, None otherwise.
        """
        try:
            data = self.serializer.loads(
                token,
                salt=self.salt,
                max_age=expiration_seconds
            )
            return data
        except Exception:
            return None
