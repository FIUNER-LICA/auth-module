from flask import Flask, render_template
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
        return render_template("inicio.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

