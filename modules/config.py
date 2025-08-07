from flask import Flask

app = Flask("server")
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env

class AppConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-por-defecto')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    
class EmailConfig:
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
