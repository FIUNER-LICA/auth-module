from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app
from modules.extensions import mail

def generate_confirmation_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')

def confirm_token(token: str, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
    except Exception:
        return None
    return email

def send_email(to_email: str, subject: str, body: str):
    msg = Message(subject=subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.body = body
    mail.send(msg)