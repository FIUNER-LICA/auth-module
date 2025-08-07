from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from modules.auth.controller import register_user, authenticate_user, verify_user

auth_bp = Blueprint('auth', __name__)

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
