from modules.app_config import EmailConfig
from sender import Mail, Message
from sender import Attachment

#################################################
# Inicio: Configuración para todos los ejemplos #
#################################################
# Configuración de conexión al servidor SMTP
SMTP_HOST = EmailConfig.MAIL_SERVER
SMTP_PORT = EmailConfig.MAIL_PORT
SMTP_USER = EmailConfig.MAIL_USERNAME
SMTP_PASS = EmailConfig.MAIL_PASSWORD
SMTP_ADDRESS = EmailConfig.MAIL_USERNAME # 'sender@example.com'
FROM_ADDR = ('No responder', SMTP_ADDRESS)   # NOTE: 'No responder' es el nombre que verá el destinatario
MAIL_USE_TLS = EmailConfig.MAIL_USE_TLS

# Dirección de correo del destinatario (para pruebas, usar tu correo electrónico personal)
recipient_email = "pepito@mail.com" # TODO: Cambiar a tu correo de prueba personal (ejemplo: "pepito@mail.com")

# Creación de objeto Mail
mail = Mail(
    host=SMTP_HOST, 
    port=SMTP_PORT, 
    username=SMTP_USER, 
    password=SMTP_PASS, 
    fromaddr=FROM_ADDR,
    use_tls=MAIL_USE_TLS)
##############################################
# Fin: Configuración para todos los ejemplos #
##############################################


#######################################################
# Inicio ejemplo 1: Envio de correo con "texto plano" #
#######################################################
# Creación de mensaje
subject  = "Correo con texto plano"
to_email = recipient_email
body     = "¡Hola email!."
msg1 = Message(subject=subject, to=to_email, body=body)

# Envío de mensaje
mail.send(msg1)
####################################################
# Fin ejemplo 1: Envio de correo con "texto plano" #
####################################################

################################################
# Inicio ejemplo 2: Envio de correo con "html" #
################################################
# Creación de mensaje
subject  = "Correo con HTML"
to_email = recipient_email
html     = "<h1>Correo con HTML</h1><p style='color:blue;'>¡Hola email!</p>"
msg2 = Message(subject=subject, to=to_email, html=html)

# Envío de mensaje
mail.send(msg2)
#############################################
# Fin ejemplo 2: Envio de correo con "html" #
#############################################

####################################################################
# Inicio ejemplo 3: Envio de correo con "html" y "archivo adjunto" #
####################################################################
# Creación de mensaje
subject  = "Correo con HTML y archivo adjunto"
to_email = recipient_email
html     = "<h1>Correo con HTML y archivo adjunto</h1><p style='color:blue;'>¡Hola email!</p>"
msg3 = Message(subject=subject, to=to_email, html=html)

with open("apps/ejemplo_00_enviar_correo_demo/logo.jpeg", mode="rb") as f:
    attachment = Attachment("logo.jpg", "image/jpeg", f.read())

msg3.attach(attachment)

# Envío de mensaje
mail.send(msg3)
#################################################################
# Fin ejemplo 3: Envio de correo con "html" y "archivo adjunto" #
#################################################################