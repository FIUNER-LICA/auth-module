"""
Unit tests for password validation and policies.
"""
from auth_module.core.security.password import PasswordPolicy, PasswordPolicyConfig, LengthRule, RegexRule, is_password_valid


def test_password_policy_default():
    """Test the default password policy which requires a minimum length of 8 characters."""
    policy = PasswordPolicy()

    is_valid, msg = policy.validate('short')
    assert not is_valid
    assert 'least 8 characters' in msg

    is_valid, msg = policy.validate('validpassword')
    assert is_valid
    assert msg == 'Password is valid.'

def test_password_policy_custom_length():
    """Test a custom password policy with a minimum length of 12 characters and custom message."""
    config = PasswordPolicyConfig(
        length=LengthRule(value=12, message='Demasiado corta: {value}')
    )
    policy = PasswordPolicy(config)

    is_valid, msg = policy.validate('12345678')
    assert not is_valid
    assert msg == 'Demasiado corta: 12'

    assert policy.validate('123456789012')[0]

def test_password_policy_regex():
    """Test a password policy that requires at least one number using a regex pattern."""
    # Require at least one number
    config = PasswordPolicyConfig(
        length=LengthRule(value=6),
        regex=RegexRule(pattern=r'^.*[0-9].*$')
    )
    policy = PasswordPolicy(config)
    assert not policy.validate('noumbers')[0]
    assert policy.validate('hasnumb3r')[0]

def test_is_password_valid():
    """Test the is_password_valid function for matching and non-matching passwords."""
    assert is_password_valid('same', 'same')
    assert not is_password_valid('same', 'different')
