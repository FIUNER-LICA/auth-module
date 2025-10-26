import os
from dotenv import load_dotenv
load_dotenv()  # Carga las variables de entorno desde el archivo .env

class AppConfig:
    """Configuración general de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False

   
class BaseUrlConfig:
    """Configuración de URLs"""
    BASE_URL = os.getenv('BASE_URL')

