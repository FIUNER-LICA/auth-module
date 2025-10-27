from modules.auth.mail_base import MailBase
from modules.auth.abs_email_server import AbsEmailServerConfig
from sender import Mail, Message, Attachment


class MailLICA(MailBase):
    def __init__(self):
        super().__init__()
        self.__mail = None

    def init_mail(self, config: AbsEmailServerConfig):
        # Configuración de conexión al servidor SMTP
        SMTP_HOST = config.mail_server
        SMTP_PORT = config.mail_port
        SMTP_USER = config.mail_username
        SMTP_PASS = config.mail_password
        SMTP_ADDRESS = config.mail_sender_address # 'sender@example.com'
        NAME_SENDER = config.name_sender
        FROM_ADDR = (NAME_SENDER, SMTP_ADDRESS)   # NOTE: NAME_SENDER es el nombre que verá el destinatario
        MAIL_USE_TLS = config.mail_use_tls

        # Creación de objeto Mail
        self.__mail = Mail(
            host=SMTP_HOST, 
            port=SMTP_PORT, 
            username=SMTP_USER, 
            password=SMTP_PASS, 
            fromaddr=FROM_ADDR,
            use_tls=MAIL_USE_TLS)
    
    def send(self, to_email: str, subject: str, body: str, logo_image_file: str = None):
        html = body # NOTE: texto plano ó HTML
        msg = Message(subject=subject, to=to_email, html=html)
        if logo_image_file is not None:
            with open(logo_image_file, mode="rb") as f:
                attachment = Attachment(logo_image_file.split('/')[-1], "image/jpeg", f.read())
            msg.attach(attachment)
        self.__mail.send(msg)


if __name__ == "__main__":
    from modules.auth.email_config import EmailConfig
    mail = MailLICA()
    e = EmailConfig()
    mail.init_mail(e)
    # Envío de mensaje de prueba
    to_email = "<nombre@mail.com>" # TODO: Cambiar a tu correo de prueba personal.
    subject  = "Correo con HTML y un logo adjunto con formato JPEG."
    html     = "<h1>Correo con HTML</h1><p style='color:blue;'>¡Hola email!</p>"
    logo_image_file = "../../apps/ejemplo_sender_00_enviar_correo/logo.jpeg"
    mail.send(to_email, subject, html, logo_image_file)

    
