"""
Unit tests for SQLite user repository.
"""
import pytest
from auth_module.core.db.sqlite_repository import SQLiteUserRepository


@pytest.fixture
def repo(tmp_path):
    """Initialize a SQLiteUserRepository with a temporary database file for testing."""
    # Use a temporary file for the database so that connections share the same data
    db_file = tmp_path / 'test_users.db'
    repository = SQLiteUserRepository(db_path=str(db_file))
    yield repository

def test_create_and_get_user(repo):
    """Test creating a user and retrieving it from the repository."""
    repo.create_user(
        email='test@example.com',
        password_hash='hashed_pw',
        verified=False,
        name='Test User'
    )

    user = repo.get_user_by_email('test@example.com')
    assert user is not None
    assert user['email'] == 'test@example.com'
    assert user['password'] == 'hashed_pw'
    assert user['verified'] is False
    assert user['name'] == 'Test User'

def test_get_nonexistent_user(repo):
    """Test retrieving a user that does not exist."""
    user = repo.get_user_by_email('nobody@example.com')
    assert user is None

def test_update_user_verification(repo):
    """Test updating a user's verification status."""
    repo.create_user('verify@example.com', 'hash', False)
    repo.update_user_verification('verify@example.com', True)

    user = repo.get_user_by_email('verify@example.com')
    assert user['verified'] is True

def test_update_user_password(repo):
    """Test updating a user's password hash."""
    repo.create_user('pwd@example.com', 'old_hash', True)
    repo.update_user_password('pwd@example.com', 'new_hash')

    user = repo.get_user_by_email('pwd@example.com')
    assert user['password'] == 'new_hash'
