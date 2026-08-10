"""
Example 03: Custom Security Policies.

This example demonstrates how to inject custom password policies and custom
hashing algorithms into the AuthManager.
"""

import os

from flask import Flask

from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.console_dispatcher import ConsoleMailDispatcher
from auth_module.core.security.password import PasswordPolicy, PasswordPolicyConfig
from auth_module.core.security.rules import LengthRule, RegexRule
from auth_module.flask_ext.extension import AuthExtension


def create_app() -> Flask:
    """
    Creates the Flask application with a custom password policy.

    Returns:
        Flask: The configured Flask app.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'development_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # Setup dependencies
    db_path = os.path.join(app.root_path, 'secure_users.db')
    user_repository = SQLiteUserRepository(db_path=db_path)
    mail_dispatcher = ConsoleMailDispatcher()

    # Create a custom password policy
    # Example: Require exactly 12 characters minimum, and force specific patterns
    # The regex below requires at least one uppercase, one lowercase, one number, and one special character
    config = PasswordPolicyConfig(
        rules=[
            LengthRule(
                value=12,
                message='La contraseña debe tener al menos {value} caracteres.'
            ),
            RegexRule(
                pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9\s]).+$',
                message='La contraseña debe incluir por lo menos 1 mayúscula, 1 minúscula, 1 número y 1 símbolo.'
            )
        ],
        msg_valid='Contraseña aceptada.'
    )
    strict_policy = PasswordPolicy(config)

    # Initialize AuthManager with the custom policy
    auth_manager = AuthManager(
        mail_dispatcher=mail_dispatcher,
        user_repository=user_repository,
        base_url='http://localhost:5000',
        secret_key=app.config['SECRET_KEY'],
        password_policy=strict_policy
        # You could also pass password_hasher=MyCustomHasher() here
    )

    # Initialize the extension
    AuthExtension(app, auth_manager)

    @app.route('/')
    def index():
        return '''
        <h1>Custom Security Example</h1>
        <p>This app requires strict passwords (12 chars, uppercase, lowercase, number, symbol).</p>
        <a href="/auth/register">Try Registering</a>
        '''

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
