from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from modules.auth.controller import register_user, authenticate_user, verify_user,create_or_get_user_oauth
from modules.auth.oauth import google, github
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/inicio')
def inicio():
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            register_user(email, password)
            flash("Revisa tu correo para verificar tu cuenta.", "success")
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template('register.html')

@auth_bp.route('/verify/<token>')
def verify(token):
    if verify_user(token):
        flash("Correo verificado, ya podés iniciar sesión.", "success")
        return redirect(url_for('auth.login'))
    else:
        flash("El enlace es inválido o expiró.", "danger")
        return redirect(url_for('auth.register'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if authenticate_user(email, password):
                session['email'] = email
                flash("Inicio de sesión exitoso.", "success")
                return redirect(url_for('auth.dashboard'))
            else:
                flash("Correo o contraseña incorrectos.", "danger")
        except ValueError as e:
            flash(str(e), "warning")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('email', None)
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash("Debes iniciar sesión para acceder.", "warning")
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', email=session['email'])

@auth_bp.route("/google")
def google_login():
    flash("Inicio de sesión con Google en desarrollo", "info")
    # if not google.authorized:
    #     return redirect(url_for("auth.google_login"))
    # resp = google.get("/oauth2/v2/userinfo")
    # user_info = resp.json()
    # create_or_get_user_oauth(email=user_info["email"], name=user_info.get("name"))
    return redirect(url_for("auth.login"))

# Login con GitHub
@auth_bp.route("/github")
def github_login():
    flash("Inicio de sesión con GitHub en desarrollo", "info")

    # if not github.authorized:
    #     return redirect(url_for("auth.github_login"))
    # resp = github.get("/user")
    # user_info = resp.json()
    # email = user_info.get("email")
    # if not email:  # A veces GitHub no da el email, hay que pedirlo aparte
    #     emails_resp = github.get("/user/emails")
    #     email = emails_resp.json()[0]["email"]
    # create_or_get_user_oauth(email=email, name=user_info.get("login"))
    return redirect(url_for("auth.login"))