from modules.auth.security import hash_password, verify_password
from modules.auth.email_verification import generate_confirmation_token, confirm_token, send_email

# Simulación base de datos simple
users_db = {}

def register_user(email, password):
    if email in users_db:
        raise ValueError("Usuario ya existe")
    pwd_hash = hash_password(password)
    users_db[email] = {'password': pwd_hash, 'verified': False}
    token = generate_confirmation_token(email)
    verify_url = f"http://localhost:5000/verify/{token}"
    send_email(email, "Confirma tu cuenta", f"Por favor confirma tu correo haciendo clic aquí: {verify_url}")
    return True

def verify_user(token):
    email = confirm_token(token)
    if not email or email not in users_db:
        return False
    users_db[email]['verified'] = True
    return True

def authenticate_user(email, password):
    user = users_db.get(email)
    if not user:
        return False
    if not user['verified']:
        raise ValueError("El correo no está verificado")
    if verify_password(password, user['password']):
        return True
    return False
