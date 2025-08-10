from flask import Flask

app = Flask("server")
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env

class AppConfig:
    """Configuración general de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    
class EmailConfig:
    """Configuración de Flask-Mail"""
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

class BaseUrlConfig:
    """Configuración de URLs"""
    BASE_URL = os.getenv('BASE_URL')