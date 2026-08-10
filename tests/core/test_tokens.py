"""
Unit tests for the TokenManager.
"""

from auth_module.core.tokens import TokenManager


def test_token_generation_and_confirmation():
    manager = TokenManager(secret_key='test_secret')
    email = 'test@example.com'

    token = manager.generate_token(email)
    assert token is not None
    assert token != email

    decoded = manager.confirm_token(token)
    assert decoded == email

def test_token_expiration():
    manager = TokenManager(secret_key='test_secret')
    token = manager.generate_token('test@example.com')

    # We test it with an expiration of 0 seconds so it immediately expires (or -1)
    decoded = manager.confirm_token(token, expiration_seconds=-1)
    assert decoded is None

def test_invalid_token():
    manager = TokenManager(secret_key='test_secret')
    decoded = manager.confirm_token('invalid.token.string')
    assert decoded is None

def test_salt_derivation_without_explicit_salt():
    manager1 = TokenManager(secret_key='secret_one')
    manager2 = TokenManager(secret_key='secret_one')
    manager3 = TokenManager(secret_key='secret_two')

    # Same secret key generates the same derived salt
    assert manager1.salt == manager2.salt

    # Different secret keys generate different derived salts
    assert manager1.salt != manager3.salt

    # Salt is not a fixed static value
    assert manager1.salt != 'email-confirm'

    assert len(manager1.salt) > 0

def test_explicit_salt():
    manager = TokenManager(secret_key='test_secret', salt='custom-salt')
    assert manager.salt == 'custom-salt'
