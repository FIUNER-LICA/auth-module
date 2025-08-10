from flask import Flask
from flask_session import Session
from flask_mail import Mail
from modules.auth.routes import auth_bp
from modules.auth.session_manager import init_session
from modules.extensions import mail
from modules.config import EmailConfig, AppConfig, BaseUrlConfig

def create_app():
    app = Flask(__name__)
    # Carga de configuraciones generales. Ver config.py
    app.config.from_object(AppConfig)

    # Carga de configuración de Flask-Mail. Ver config.py
    app.config.from_object(EmailConfig)

    app.config.from_object(BaseUrlConfig)  # Carga de configuración de URLs
    
    init_session(app)
    mail.init_app(app)  # inicializa mail con app

    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return "Portal de Autorización del LICA"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

# from flask import Flask, redirect, url_for, session
# from flask_dance.contrib.google import make_google_blueprint, google
# import os

# app = Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

# # Credenciales desde variables de entorno (creadas en Google Cloud Console)
# GOOGLE_CLIENT_ID = os.getenv("69678492292-ugsphlfg3pfq1sbseg2bh8m2ofuaelj1.apps.googleusercontent.com")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# blueprint = make_google_blueprint(
#     client_id=GOOGLE_CLIENT_ID,
#     client_secret=GOOGLE_CLIENT_SECRET,
#     scope=["profile", "email"],
#     redirect_to="google_login"
# )
# app.register_blueprint(blueprint, url_prefix="/login")

# @app.route("/")
# def index():
#     if not google.authorized:
#         return '<a href="/login/google">Iniciar sesión con Google</a>'
#     resp = google.get("/oauth2/v2/userinfo")
#     assert resp.ok, resp.text
#     user_info = resp.json()
#     return f"""
#     <h1>Hola, {user_info['name']}</h1>
#     <p>Email: {user_info['email']}</p>
#     <a href="/logout">Cerrar sesión</a>
#     """

# @app.route("/google_login")
# def google_login():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     return redirect(url_for("index"))

# @app.route("/logout")
# def logout():
#     token = blueprint.token
#     if token:
#         del blueprint.token  # elimina token en sesión
#     session.clear()
#     return redirect(url_for("index"))

# if __name__ == "__main__":
#     app.run(debug=True)
