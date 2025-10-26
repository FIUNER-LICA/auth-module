import os
from dotenv import load_dotenv
from modules.auth.abs_email_server import AbsEmailServerConfig

load_dotenv()  # Carga las variables de entorno desde el archivo .env    


class EmailConfig(AbsEmailServerConfig):
    """Configuración del servidor de envío de correo"""
    
    # MAIL_SERVER = os.getenv('MAIL_SERVER')
    # MAIL_PORT = int(os.getenv('MAIL_PORT'))
    # NAME_SENDER = os.getenv('NAME_SENDER')      # NOTE: NAME_SENDER es el nombre que verá el destinatario
    # MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_SENDER_ADDRESS = os.getenv('MAIL_SENDER_ADDRESS')

    @property 
    def mail_server(self):
        return os.getenv('MAIL_SERVER')
    
    @property
    def mail_port(self):
        return int(os.getenv('MAIL_PORT'))

    @property 
    def mail_username(self):
        return os.getenv('MAIL_USERNAME')
    
    @property
    def mail_password(self):
        return os.getenv('MAIL_PASSWORD')
    
    @property
    def mail_sender_address(self):
        return os.getenv('MAIL_SENDER_ADDRESS')
    
    @property 
    def name_sender(self):
        return os.getenv('NAME_SENDER')
    
    @property 
    def mail_sender_address(self):
        return os.getenv('MAIL_SENDER_ADDRESS')
    
    @property 
    def mail_use_tls(self):
        return os.getenv('MAIL_USE_TLS') == 'True'
    