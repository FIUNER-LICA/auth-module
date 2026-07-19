# Módulo de Autenticación

Un módulo de autenticación robusto, agnóstico y altamente modular, diseñado para ser consumido como un paquete instalable en proyectos de Python.

El módulo provee una base sólida (Core) que gestiona toda la lógica de validación de contraseñas, hashing, interacción con bases de datos configurable (SQLite por defecto) y envío de correos electrónicos. Además, incluye una extensión opcional y completa para Flask, que aporta las rutas y plantillas listas para usar.

## Características Principales

- Agnóstico por Diseño: Toda la lógica de negocio ([AuthManager](src/auth_module/core/auth_manager.py)) es independiente de cualquier framework web.
- Extensión para Flask: Blueprints y templates listos para el registro, login, y recuperación de contraseñas en la carpeta [flask_ext](src/auth_module/flask_ext).
- Seguridad Configurable: Políticas de contraseñas inyectables y soporte para Hashing adaptativo en la carpeta [security](src/auth_module/core/security).
- Despachador de Correo Intercambiable: Diferentes adaptadores como SMTP puro o despachador en consola para desarrollo en la carpeta [mail](src/auth_module/core/mail).

---

## Instalación y Uso en Proyectos Externos

Como este paquete fue diseñado como una librería, la mejor forma de integrarlo en tu proyecto es a través de `pip`, tratándolo como una dependencia local.

### 1. Clonar el repositorio
Clona este repositorio dentro del directorio de tu proyecto principal (por ejemplo, dentro de una carpeta llamada `libs/` o `deps/`).

```bash
mkdir libs
cd libs
git clone <https://github.com/FIUNER-LICA/auth-module> auth-module
```

### 2. Ignorar la carpeta en tu control de versiones
Es muy importante que agregues esta carpeta al `.gitignore` de tu proyecto principal para no trackear repositorios anidados accidentalmente.

Agrega esto a tu archivo `.gitignore`:
```text
# Ignorar dependencias locales
libs/auth-module/
# O si usaste deps:
# deps/auth-module/
```

### 3. Instalar con pip
Activa el entorno virtual de tu proyecto principal e instala el módulo. 

Instalación Básica (Solo Core, sin Flask):
```bash
pip install ./libs/auth-module
```

Instalación con Flask (Incluye dependencias web y vistas):
```bash
pip install "./libs/auth-module[flask]"
```
*(Nota: Usar la bandera `-e` durante el `pip install` es útil si planeas modificar el código del módulo auth-module y ver los cambios reflejados instantáneamente en tu proyecto).*

---

## Inicio Rápido

El paquete incluye una carpeta [examples/](examples) en la raíz del proyecto con el código listo para ejecutarse. A continuación se presentan los conceptos clave:

### Uso Puro (Solo Backend)
Ver el ejemplo completo en: [examples/01_core_backend/main.py](examples/01_core_backend/main.py)

```python
from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.console_dispatcher import ConsoleMailDispatcher

# 1. Base de Datos
repo = SQLiteUserRepository(db_path='/ruta/absoluta/usuarios.db')

# 2. Despachador de Correos (Consola para desarrollo)
mail = ConsoleMailDispatcher()

# 3. Manager Principal
auth_manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost',
    secret_key='mi_secreto'
)

# Uso
auth_manager.register_user('hola@ejemplo.com', 'PassSeguro123!')
```

### Uso con Flask
Ver el ejemplo completo en: [examples/02_flask_extension/app.py](examples/02_flask_extension/app.py)

```python
from flask import Flask
from auth_module.flask_ext.extension import AuthExtension
# ... importar repo y mail_dispatcher ...

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto'
app.config['SESSION_TYPE'] = 'filesystem'

# Configurar el Manager y pasarlo a la Extensión
manager = AuthManager(
    mail_dispatcher=mail, 
    user_repository=repo, 
    base_url='http://localhost:5000', 
    secret_key=app.config['SECRET_KEY']
)
AuthExtension(app, manager)

# El blueprint de /auth ya está registrado y listo para usarse.
```

---

## Estructura del Proyecto

- [src/auth_module/core/](src/auth_module/core): Toda la lógica base (Base de datos, Hashing, Correo, Tokens).
- [src/auth_module/flask_ext/](src/auth_module/flask_ext): Extensión de Flask (Rutas, Decoradores, Templates, Estilos).
- [examples/](examples): Ejemplos detallados de implementación (Core backend, Flask extension, Custom security).
- [tests/](tests): Pruebas unitarias modulares.
- [pyproject.toml](pyproject.toml): Definición del paquete y dependencias.

---

## Testing

El proyecto cuenta con pruebas automáticas bajo la carpeta [tests/](tests). Para correrlas todas:

```bash
# Instalar dependencias de desarrollo
pip install "./libs/auth-module[dev]"

# Ejecutar pytest
pytest libs/auth-module/tests/
```
