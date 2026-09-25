"""
Example 01: Core Backend Usage.

This example demonstrates how to use the AuthManager independently of Flask,
as a standalone library for authentication logic, database management, and email dispatch.
"""

import os

from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.dispatchers import ConsoleMailDispatcher


def main():
    """Main function to execute the core backend example."""
    print('--- Core Backend Example ---')

    # 1. Define the database path (must be an absolute or explicitly relative path)
    db_path = os.path.join(os.getcwd(), 'example_users.db')
    print(f'Using database at: {db_path}')

    # 2. Initialize the repository
    user_repository = SQLiteUserRepository(db_path=db_path)

    # 3. Configure the email dispatcher
    # For this example, we use the ConsoleMailDispatcher to avoid needing real SMTP credentials
    # In production, you would import SmtpMailDispatcher and EmailEnvConfig
    mail_dispatcher = ConsoleMailDispatcher()

    # 4. Initialize the AuthManager
    auth_manager = AuthManager(
        mail_dispatcher=mail_dispatcher,
        user_repository=user_repository,
        base_url='http://localhost:5000',
        secret_key='super_secret_key_for_tokens'
    )

    # 5. Example operation: Register a user
    test_email = 'testuser@example.com'
    test_password = 'MySecurePassword123!'

    try:
        print(f'Attempting to register user: {test_email}')
        auth_manager.register_user(test_email, test_password)
        print('User registered successfully! A verification email was generated.')
    except ValueError as e:
        print(f'Registration failed (possibly already registered): {e}')

    # 6. Example operation: Authenticate the user
    # NOTE: Authentication will fail here because the user is not verified yet
    print(f'Attempting to authenticate user: {test_email}')
    try:
        is_authenticated = auth_manager.authenticate_user(test_email, test_password)
        print(f'Authentication result: {is_authenticated}')
    except ValueError as e:
        print(f'Authentication failed as expected: {e}')

    # Let's manually verify the user
    print('Manually verifying user to test authentication...')
    user_repository.update_user_verification(test_email, True)

    # Try authenticating again
    is_authenticated = auth_manager.authenticate_user(test_email, test_password)
    print(f'Authentication result after verification: {is_authenticated}')


if __name__ == '__main__':
    main()
