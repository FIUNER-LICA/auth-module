from flask import Flask, render_template
from flask_session import Session
from modules.auth.routes import auth_bp
from modules.auth.session_manager import init_session
from modules.auth.extensions import mail
from modules.auth.config import EmailConfig, AppConfig, BaseUrlConfig

def create_app():
    # Carga de configuración de Mail. Ver config.py
    mail.init_mail(EmailConfig)

    app = Flask(__name__)

    # Carga de configuraciones generales. Ver config.py
    app.config.from_object(AppConfig)
    app.register_blueprint(auth_bp)

    init_session(app) 

    @app.route('/')
    def index():
        return render_template("inicio.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

