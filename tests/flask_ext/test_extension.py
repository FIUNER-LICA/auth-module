"""
Unit tests for the Flask FlaskExtension.
"""

import pytest
from cachelib import SimpleCache
from flask import Flask

from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.base import MailDispatcher
from auth_module.flask_ext.extension import FlaskExtension


class MockMailDispatcher(MailDispatcher):
    def send(self, to_email: str, subject: str, body: str, logo_image_file: str | None = None) -> bool:
        return True


@pytest.fixture
def auth_manager(tmp_path):
    db_file = tmp_path / 'test_users.db'
    repo = SQLiteUserRepository(db_path=str(db_file))
    mail = MockMailDispatcher()
    return AuthManager(
        mail_dispatcher=mail,
        user_repository=repo,
        base_url='http://localhost:5000',
        secret_key='test_secret_key'
    )

def test_extension_initialization(auth_manager):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    app.config['SESSION_TYPE'] = 'cachelib'
    app.config['SESSION_CACHELIB'] = SimpleCache()

    # Initialize extension
    extension = FlaskExtension(app, auth_manager)

    # Check that it registers the auth module correctly
    assert 'auth_module' in app.extensions
    assert app.extensions['auth_module'] is auth_manager

    # Check that the blueprint is registered
    assert 'auth' in app.blueprints


def test_extension_i18n_custom_locale(auth_manager):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    app.config['SESSION_TYPE'] = 'cachelib'
    app.config['SESSION_CACHELIB'] = SimpleCache()
    app.config['AUTH_FRONTEND_LOCALE'] = 'en'

    # Initialize extension with 'en' locale override
    extension = FlaskExtension(app, auth_manager)

    assert extension.i18n.get_locale() == 'en'
    # Test English translation lookup
    assert extension.i18n.translate('email') == 'Email Address'


def test_extension_i18n_custom_translations(auth_manager):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    app.config['SESSION_TYPE'] = 'cachelib'
    app.config['SESSION_CACHELIB'] = SimpleCache()

    custom_translations = {
        'es': {
            'email': 'Dirección de Correo'
        }
    }

    # Initialize extension with custom translations
    extension = FlaskExtension(app, auth_manager, locale='es', custom_translations=custom_translations)

    assert extension.i18n.translate('email') == 'Dirección de Correo'

    # Fallback key still works
    assert extension.i18n.translate('password') == 'Contraseña'
