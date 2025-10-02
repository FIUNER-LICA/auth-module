# auth_module.py
class AuthModule:
    def __init__(self, title="Sistema de Usuarios"):
        self.title = title
        self.users = {}  # {username: password} (solo demo, sin hashing!)

    def render_register_form(self, action_url="/auth/register"):
        return f"""
        <h2>{self.title} - Registro</h2>
        <form action="{action_url}" method="post">
            <input type="text" name="username" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit">Registrar</button>
        </form>
        """

    def render_login_form(self, action_url="/auth/login"):
        return f"""
        <h2>{self.title} - Login</h2>
        <form action="{action_url}" method="post">
            <input type="text" name="username" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit">Ingresar</button>
        </form>
        """

    def register_user(self, data):
        """Procesa un dict con 'username' y 'password'"""
        username = data.get("username")
        password = data.get("password")
        if username in self.users:
            return False, "Usuario ya existe"
        self.users[username] = password
        return True, f"Usuario {username} registrado!"

    def authenticate(self, data):
        username = data.get("username")
        password = data.get("password")
        if self.users.get(username) == password:
            return True, f"Bienvenido {username}"
        return False, "Usuario o contraseña inválidos"
