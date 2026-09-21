"""
Unit tests for the TokenManager.
"""

from auth_module.core.tokens import TokenManager


def test_token_generation_and_confirmation():
    manager = TokenManager(secret_key='test_secret')
    email = 'test@example.com'
    token = manager.generate_token({'email': email, 'purpose': 'any'})

    # Assert token is returned as string
    assert isinstance(token, str)
    assert len(token) > 0

    # Assert we can extract data correctly
    extracted = manager.confirm_token(token)
    assert extracted == {'email': email, 'purpose': 'any'}

def test_token_expiration():
    """Test that tokens expire correctly."""
    manager = TokenManager(secret_key='test-secret')
    token = manager.generate_token({'email': 'test@example.com'})

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
    assert manager1._TokenManager__salt == manager2._TokenManager__salt

    # Different secret keys generate different derived salts
    assert manager1._TokenManager__salt != manager3._TokenManager__salt

    # Salt is not a fixed static value
    assert manager1._TokenManager__salt != 'email-confirm'

    assert len(manager1._TokenManager__salt) > 0

def test_explicit_salt():
    manager = TokenManager(secret_key='test_secret', salt='custom-salt')
    assert manager._TokenManager__salt == 'custom-salt'
