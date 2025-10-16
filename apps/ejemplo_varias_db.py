from functools import wraps
from flask import Flask, request, jsonify, session

# ===== MÓDULO DE AUTENTICACIÓN INDEPENDIENTE =====

class AuthSystem:
    def __init__(self):
        # Base de datos principal de usuarios (simulada con diccionario)
        self.users_db = {
            'usuario1': {'password': 'clave123', 'email': 'user1@example.com', 'id': 1},
            'usuario2': {'password': 'clave456', 'email': 'user2@example.com', 'id': 2},
            'admin': {'password': 'admin123', 'email': 'admin@example.com', 'id': 3}
        }
        
        # Diccionario para almacenar conexiones a otras bases de datos
        self.external_dbs = {}
    
    def register_external_db(self, db_name, db_connection):
        """Registra una conexión a una base de datos externa"""
        self.external_dbs[db_name] = db_connection
    
    def authenticate(self, username, password):
        """Autentica un usuario y devuelve sus datos"""
        user_data = self.users_db.get(username)
        if user_data and user_data['password'] == password:
            return {
                'username': username,
                'email': user_data['email'],
                'id': user_data['id']
            }
        return None
    
    def get_user_external_data(self, username, db_name):
        """Obtiene datos de un usuario desde una base de datos externa"""
        if db_name not in self.external_dbs:
            return None
        
        user_id = self.users_db.get(username, {}).get('id')
        if not user_id:
            return None
        
        # Simulamos obtener datos usando el ID como clave foránea
        external_db = self.external_dbs[db_name]
        return external_db.get(user_id)

# Instancia global del sistema de autenticación
auth_system = AuthSystem()

# Decorador para verificar autenticación
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si el usuario está en sesión
        if 'user' not in session:
            return jsonify({'error': 'Se requiere autenticación'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Decorador para obtener datos de bases de datos externas
def with_external_data(db_names=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            username = session.get('user')
            if not username:
                return jsonify({'error': 'Usuario no autenticado'}), 401
            
            # Obtener datos de las bases de datos externas
            external_data = {}
            for db_name in db_names:
                data = auth_system.get_user_external_data(username, db_name)
                if data is not None:
                    external_data[db_name] = data
            
            # Pasar los datos externos a la función
            kwargs['external_data'] = external_data
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ===== APLICACIÓN FLASK =====

app = Flask(__name__)
app.secret_key = 'clave_secreta_muy_segura'

# ===== BASES DE DATOS EXTERNAS (SIMULADAS) =====

# Base de datos de perfil de usuario
user_profiles_db = {
    1: {'nombre_completo': 'Juan Pérez', 'edad': 30, 'pais': 'México'},
    2: {'nombre_completo': 'María García', 'edad': 25, 'pais': 'España'},
    3: {'nombre_completo': 'Admin User', 'edad': 35, 'pais': 'Argentina'}
}

# Base de datos de pedidos
user_orders_db = {
    1: [
        {'order_id': 101, 'producto': 'Laptop', 'total': 1200},
        {'order_id': 102, 'producto': 'Mouse', 'total': 25}
    ],
    2: [
        {'order_id': 201, 'producto': 'Tablet', 'total': 300}
    ],
    3: []
}

# Registrar las bases de datos externas en el sistema de autenticación
auth_system.register_external_db('profile', user_profiles_db)
auth_system.register_external_db('orders', user_orders_db)

# ===== RUTAS DE LA APLICACIÓN =====

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = auth_system.authenticate(username, password)
    if user:
        session['user'] = username
        return jsonify({
            'message': 'Login exitoso',
            'user': user
        })
    
    return jsonify({'error': 'Credenciales inválidas'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logout exitoso'})

@app.route('/profile')
@login_required
@with_external_data(['profile', 'orders'])
def user_profile(external_data):
    """Endpoint que muestra datos del usuario desde múltiples bases de datos"""
    username = session['user']
    user_data = auth_system.users_db[username]
    
    return jsonify({
        'usuario': username,
        'email': user_data['email'],
        'perfil': external_data.get('profile', {}),
        'pedidos': external_data.get('orders', [])
    })

@app.route('/dashboard')
@login_required
@with_external_data(['profile'])
def dashboard(external_data):
    """Endpoint que solo necesita datos del perfil"""
    username = session['user']
    
    return jsonify({
        'mensaje': f'Bienvenido al dashboard, {username}',
        'perfil': external_data.get('profile', {})
    })

@app.route('/protected')
@login_required
def protected_route():
    """Endpoint que solo requiere autenticación básica"""
    return jsonify({
        'message': 'Esta es una ruta protegida',
        'user': session['user']
    })

if __name__ == '__main__':
    app.run(debug=True)