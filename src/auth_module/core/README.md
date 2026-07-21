# Documentación del Core

El directorio `core/` contiene toda la lógica agnóstica de negocio del Módulo de Autenticación. Esto significa que ninguna clase de este paquete depende de un framework web (como Flask o Django).

## Componentes Principales

### 1. AuthManager (`auth_manager.py`)
Es el orquestador principal. Utiliza Inyección de Dependencias para interactuar con la base de datos, el gestor de contraseñas y el servicio de correos.

```python
manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='secreto'
)
```
Provee métodos listos para usar como:
- `register_user(email, password)`
- `authenticate_user(email, password)`
- `verify_user(token)`
- `request_password_recovery(email)`

### 2. Base de Datos (`db/`)
Define la interfaz `UserRepository` que garantiza que cualquier implementación de base de datos expondrá los métodos necesarios (`create_user`, `get_user_by_email`, etc.).
Se provee una implementación por defecto: `SQLiteUserRepository`, ideal para un despliegue rápido sin infraestructura compleja.

### 3. Gestor de Tokens (`tokens.py`)
Utiliza `itsdangerous` para la generación segura de JWT tokens usados en:
- Verificación de correo electrónico.
- Recuperación de contraseñas.
Los tokens están cifrados y tienen un tiempo de expiración.
