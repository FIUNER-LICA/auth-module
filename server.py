from flask import Flask, render_template
from flask_session import Session
from modules.auth.routes import auth_bp, set_login_redirect
from modules.auth.session_manager import init_session
from modules.auth.extensions import mail
from modules.app_config import AppConfig
from modules.auth.email_config import EmailConfig
#  from modules.auth.config import mail_server
from modules.auth.decorators import login_required

# Carga de configuración de Mail. Ver config.py
e=EmailConfig()
mail.init_mail(e)


def create_app():
    
    app = Flask(__name__)

    # Carga de configuraciones generales. Ver config.py
    app.config.from_object(AppConfig)
    
    # cuando se autentica, esta función fija a dónde direccionar
    set_login_redirect('dashboard')

    app.register_blueprint(auth_bp)

    init_session(app) 

    @app.route('/')
    def index():
        return render_template("inicio.html")
    
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

