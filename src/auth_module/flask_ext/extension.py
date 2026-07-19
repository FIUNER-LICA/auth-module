"""
Flask extension initialization.
"""

from flask import Flask
from flask_session import Session

from ..core.auth_manager import AuthManager
from .routes import auth_bp


class AuthExtension:
    """
    Flask extension to integrate the AuthManager and authentication routes.
    """

    def __init__(self, app: Flask | None = None, auth_manager: AuthManager | None = None):
        """
        Initializes the extension.

        Args:
            app (Flask | None): The Flask application instance.
            auth_manager (AuthManager | None): The configured AuthManager instance.
        """
        self.auth_manager = auth_manager
        if app is not None:
            self.init_app(app, auth_manager)

    def init_app(self, app: Flask, auth_manager: AuthManager | None = None):
        """
        Registers the extension with the Flask application.

        Args:
            app (Flask): The Flask application instance.
            auth_manager (AuthManager | None): The configured AuthManager instance.
        """
        if auth_manager:
            self.auth_manager = auth_manager

        if not self.auth_manager:
            raise ValueError('An AuthManager instance must be provided to AuthExtension.')

        # Store the manager in app extensions for route access
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['auth_module'] = self.auth_manager

        # Initialize Flask-Session if it's not already initialized
        if 'session' not in app.extensions:
            Session(app)

        # Register the authentication blueprint
        app.register_blueprint(auth_bp, url_prefix='/auth')
