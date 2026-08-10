"""
Unit tests for password hasher implementations.
"""

from auth_module.core.security.hasher import WerkzeugPasswordHasher


def test_werkzeug_password_hasher():
    """Test the WerkzeugPasswordHasher for hashing and verifying passwords."""
    hasher = WerkzeugPasswordHasher()
    password = 'MySecurePassword123'

    hashed = hasher.hash(password)
    assert hashed != password
    assert hashed.startswith(('scrypt:', 'pbkdf2:'))

    assert hasher.verify(password, hashed)
    assert not hasher.verify('wrongpassword', hashed)
