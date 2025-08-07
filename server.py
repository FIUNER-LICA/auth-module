from flask import Flask
from flask_session import Session
from flask_mail import Mail
from modules.auth.routes import auth_bp
from modules.auth.session_manager import init_session
from modules.extensions import mail
from modules.config import EmailConfig, AppConfig

def create_app():
    app = Flask(__name__)
    # Carga de configuraciones generales. Ver config.py
    app.config.from_object(AppConfig)

    # Carga de configuración de Flask-Mail. Ver config.py
    app.config.from_object(EmailConfig)
    
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
