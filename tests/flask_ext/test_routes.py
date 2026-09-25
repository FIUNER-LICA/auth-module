"""
Unit tests for Flask routes.
"""

import pytest
from cachelib import SimpleCache
from flask import Flask

from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.dispatchers.base import MailDispatcher
from auth_module.flask_ext.extension import FlaskExtension


class MockMailDispatcher(MailDispatcher):
    def send(self, to_email: str, subject: str, body: str) -> bool:
        return True


@pytest.fixture
def test_client(tmp_path):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    app.config['SESSION_TYPE'] = 'cachelib'
    app.config['SESSION_CACHELIB'] = SimpleCache()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Probar sin CSRF tokens

    db_file = tmp_path / 'test_users.db'
    repo = SQLiteUserRepository(db_path=str(db_file))
    mail = MockMailDispatcher()

    auth_manager = AuthManager(
        mail_dispatcher=mail,
        user_repository=repo,
        base_url='http://localhost:5000',
        secret_key='test_secret_key'
    )

    FlaskExtension(app, auth_manager, login_redirect_endpoint='dummy_dashboard')

    @app.route('/dummy')
    def dummy_dashboard():
        return 'Dashboard'

    with app.test_client() as client, app.app_context():
        yield client, auth_manager


def test_login_get(test_client):
    client, _ = test_client
    response = client.get('/auth/login')
    assert response.status_code == 200


def test_register_get(test_client):
    client, _ = test_client
    response = client.get('/auth/register')
    assert response.status_code == 200


def test_register_post(test_client):
    client, manager = test_client
    response = client.post('/auth/register', data={
        'email': 'newuser@test.com',
        'password': 'Password123!',
        'repassword': 'Password123!'
    })
    # After register, redirects to login
    assert response.status_code == 302
    assert manager._AuthManager__user_repository.get_user_by_email('newuser@test.com') is not None


def test_login_post(test_client):
    client, manager = test_client
    manager.register_user('user@test.com', 'Password123!')
    manager._AuthManager__user_repository.update_user_verification('user@test.com', True)

    response = client.post('/auth/login', data={
        'email': 'user@test.com',
        'password': 'Password123!'
    })
    # On success, redirects to redirect_endpoint
    assert response.status_code == 302
    assert response.location.endswith('/dummy')


def test_verify_route(test_client):
    client, manager = test_client
    manager.register_user('verify@test.com', 'Password123!')

    token = manager._AuthManager__token_manager.generate_token({'email': 'verify@test.com', 'purpose': 'verification'})

    response = client.get(f'/auth/verify/{token}')
    assert response.status_code == 302
    assert manager._AuthManager__user_repository.get_user_by_email('verify@test.com')['verified'] is True


def test_logout(test_client):
    client, _ = test_client
    response = client.get('/auth/logout')
    assert response.status_code == 302
