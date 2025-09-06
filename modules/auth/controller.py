
from modules.auth.security import hash_password, verify_password,is_password_strong, is_password_valid
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

def create_or_get_user_oauth(email, name=None, provider=None):
    """
    Si el usuario no existe, lo crea marcado como verificado (porque viene de OAuth).
    Devuelve el dict del usuario.
    """
    user = users_db.get(email)
    if user:
        return user
    users_db[email] = {'password': None, 'verified': True, 'name': name, 'oauth': provider}
    return users_db[email]

def send_password_recovery_email(email):
    if email not in users_db:
        raise ValueError("No existe usuario con ese correo")
    else:
        token = generate_confirmation_token(email)
        recovery_url = f"http://localhost:5000/reset_password/{token}"
        send_email(email, "Recuperación de contraseña", f"Para restablecer tu contraseña, haz clic aquí: {recovery_url}")
        return True
    
def is_a_valid_password(password: str, repassword:str) -> tuple[bool,str]:
    """
    Verifica si la contraseña cumple con la regla y si son contraseñas son iguales .
    """
    message = "La contraseña es válida."
    result = True
    if not is_password_strong(password):
        message = "La contraseña debe tener al menos 8 caracteres."
        result = False
    elif not is_password_valid(password, repassword):
        message = "Las contraseñas no coinciden."
        result = False

    return result, message