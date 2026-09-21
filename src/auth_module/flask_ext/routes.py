"""
Flask routes for the authentication module.
"""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .decorators import login_required
from .forms import LoginForm, PasswordRecoveryForm, PasswordResetForm, RegisterForm

# Create a blueprint with template and static folders configured to point to this package's folders
auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Configurable redirect endpoint after successful login
_LOGIN_REDIRECT_ENDPOINT = 'auth.auth_dashboard'

def _set_login_redirect(endpoint: str):
    """
    Sets the endpoint to redirect to after a successful login.
    """
    global _LOGIN_REDIRECT_ENDPOINT
    _LOGIN_REDIRECT_ENDPOINT = endpoint


def get_auth_manager():
    """Helper to get the auth_manager from the current Flask app."""
    return current_app.extensions['auth_module']


def _t(key: str, **kwargs) -> str:
    """
    Helper to translate a frontend key using the registered frontend translator.

    Args:
        key (str): The translation key.
        **kwargs: Additional keyword arguments for formatting the translation string.

    Returns:
        str: The translated string.
    """
    translator = current_app.extensions.get('auth_frontend_i18n')
    if translator:
        return translator.translate(key, **kwargs)
    return key


@auth_bp.context_processor
def inject_i18n():
    """Injects the 't' function into Jinja templates for localization."""
    return {'t': _t}


def _flash_form_errors(form):
    """Flashes WTForms validation errors."""
    for errors in form.errors.values():
        for error in errors:
            flash(_t(error), 'danger')


@auth_bp.route('/home')
def home():
    """Redirects to the index page."""
    return redirect(url_for('index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            auth_manager = get_auth_manager()
            try:
                auth_manager.register_user(email, password)
                flash(_t('flash_check_email_verify'), 'success')
                return redirect(url_for('auth.login'))
            except ValueError as e:
                flash(str(e), 'danger')

        else:
            _flash_form_errors(form)

    return render_template('register.html', form=form)


@auth_bp.route('/password-recovery', methods=['GET', 'POST'])
def password_recovery():
    """Handles password recovery requests."""
    form = PasswordRecoveryForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            auth_manager = get_auth_manager()

            auth_manager.request_password_recovery(email)
            flash(_t('flash_recovery_link_sent'), 'info')
            return redirect(url_for('auth.login'))

        else:
            _flash_form_errors(form)

    return render_template('password_recovery.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def pw_reset_token(token):
    """Verifies a password reset token and handles the reset."""
    auth_manager = get_auth_manager()
    form = PasswordResetForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            password = form.password.data

            try:
                auth_manager.reset_password(token, password)
                flash(_t('flash_password_updated'), 'success')
                return redirect(url_for('auth.login'))
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('password_reset.html', token=token, form=form)

        else:
            _flash_form_errors(form)

    # GET request: verify token before showing form
    if auth_manager.verify_password_reset_token(token):
        return render_template('password_reset.html', token=token, form=form)

    flash(_t('flash_link_invalid_expired'), 'danger')
    return redirect(url_for('auth.login'))


@auth_bp.route('/verify/<token>')
def verify(token):
    """Verifies a user's email."""
    auth_manager = get_auth_manager()

    if auth_manager.verify_user(token):
        flash(_t('flash_email_verified_login'), 'success')
        return redirect(url_for('auth.login'))

    flash(_t('flash_link_invalid_expired'), 'danger')
    return redirect(url_for('auth.register'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            auth_manager = get_auth_manager()

            try:
                if auth_manager.authenticate_user(email, password):
                    session['email'] = email
                    flash(_t('flash_login_successful'), 'success')
                    return redirect(url_for(_LOGIN_REDIRECT_ENDPOINT))

                flash(_t('flash_incorrect_credentials'), 'danger')
            except ValueError as e:
                flash(str(e), 'warning')

        else:
            _flash_form_errors(form)

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('email', None)
    flash(_t('flash_logged_out'), 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/auth-default-dashboard')
@login_required
def auth_dashboard():
    """A default protected dashboard route."""
    return render_template('auth_default_dashboard.html')
