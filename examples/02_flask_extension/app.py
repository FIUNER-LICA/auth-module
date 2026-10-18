"""
Example 02: Flask Extension Usage.

This example demonstrates how to integrate the auth-module into a Flask application
using the provided FlaskExtension and blueprints.
"""

import os

from flask import Flask

from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.dispatchers import ConsoleMailDispatcher
from auth_module.flask_ext.decorators import login_required
from auth_module.flask_ext.extension import FlaskExtension


def create_app() -> Flask:
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask app.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'development_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # 1. Configure the core dependencies
    db_path = os.path.join(app.root_path, 'flask_users.db')
    user_repository = SQLiteUserRepository(db_path=db_path)

    # Email configuration
    # Using ConsoleMailDispatcher for the example so it prints to terminal
    mail_dispatcher = ConsoleMailDispatcher()

    # 2. Initialize the AuthManager
    auth_manager = AuthManager(
        mail_dispatcher=mail_dispatcher,
        user_repository=user_repository,
        base_url='http://localhost:5000/auth',
        secret_key=app.config['SECRET_KEY']
    )

    # 3. Initialize the Flask extension
    # This automatically registers the '/auth' blueprint and configures the session
    # We pass login_redirect_endpoint to configure where the user is redirected to after a successful login
    FlaskExtension(app, auth_manager, login_redirect_endpoint='dashboard')

    # 4. Define application routes
    @app.route('/')
    def index():
        return '''
        <h1>Welcome to the Flask Example</h1>
        <a href="/auth/login">Login</a> | <a href="/auth/register">Register</a>
        '''

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return '''
        <h1>Dashboard</h1>
        <p>You are logged in!</p>
        <a href="/auth/logout">Logout</a>
        '''

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
