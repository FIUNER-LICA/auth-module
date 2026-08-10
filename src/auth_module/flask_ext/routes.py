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

# Create a blueprint with template and static folders configured to point to this package's folders
auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Configurable redirect endpoint after successful login
_LOGIN_REDIRECT_ENDPOINT = 'auth.auth_dashboard'

def set_login_redirect(endpoint: str):
    """
    Sets the endpoint to redirect to after a successful login.
    """
    global _LOGIN_REDIRECT_ENDPOINT
    _LOGIN_REDIRECT_ENDPOINT = endpoint


def get_auth_manager():
    """Helper to get the auth_manager from the current Flask app."""
    return current_app.extensions['auth_module']


@auth_bp.route('/home')
def home():
    """Redirects to the index page."""
    return redirect(url_for('index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        auth_manager = get_auth_manager()

        try:
            auth_manager.register_user(email, password)
            flash('Please check your email to verify your account.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'danger')

    return render_template('register.html')


@auth_bp.route('/password-recovery', methods=['GET', 'POST'])
def password_recovery():
    """Handles password recovery requests."""
    if request.method == 'POST':
        email = request.form.get('email')
        auth_manager = get_auth_manager()

        try:
            auth_manager.request_password_recovery(email)
            flash('If the email exists, a recovery link has been sent.', 'info')
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('auth.login'))

        return render_template('password_recovery.html')

    return render_template('password_recovery.html')


@auth_bp.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    """Handles the password reset process after clicking a recovery link."""
    if request.method == 'POST':
        if session.get('pw_reset_number_access_to_pw_reset', 0) > 0:
            flash('Password reset session expired.', 'danger')
            return redirect(url_for('auth.login'))

        session['pw_reset_number_access_to_pw_reset'] = session.get('pw_reset_number_access_to_pw_reset', 0) + 1

        email = session.get('pw_reset_email')
        password = request.form.get('password')

        auth_manager = get_auth_manager()

        try:
            auth_manager.reset_password(email, password)
            flash('Password updated successfully.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'danger')

        return render_template('login.html')

    return render_template('password_reset.html')


@auth_bp.route('/reset-password/<token>')
def pw_reset_token(token):
    """Verifies a password reset token."""
    auth_manager = get_auth_manager()
    email = auth_manager.verify_password_reset_token(token)

    if email:
        session['pw_reset_email'] = email
        session['pw_reset_number_access_to_pw_reset'] = 0
        flash('Email verified. You can now set your new password.', 'success')
        return redirect(url_for('auth.password_reset'))

    flash('The link is invalid or has expired.', 'danger')
    return redirect(url_for('auth.login'))


@auth_bp.route('/verify/<token>')
def verify(token):
    """Verifies a user's email."""
    auth_manager = get_auth_manager()

    if auth_manager.verify_user(token):
        flash('Email verified, you can now log in.', 'success')
        return redirect(url_for('auth.login'))

    flash('The link is invalid or has expired.', 'danger')
    return redirect(url_for('auth.register'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        auth_manager = get_auth_manager()

        try:
            if auth_manager.authenticate_user(email, password):
                session['email'] = email
                flash('Login successful.', 'success')
                return redirect(url_for(_LOGIN_REDIRECT_ENDPOINT))

            flash('Incorrect email or password.', 'danger')
        except ValueError as e:
            flash(str(e), 'warning')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('email', None)
    flash('You have logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/auth-default-dashboard')
@login_required
def auth_dashboard():
    """A default protected dashboard route."""
    return render_template('auth_default_dashboard.html')
