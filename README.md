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

Instalación con Flask y OAuth (Funcionalidades web completas):
```bash
pip install "./libs/auth-module[flask,oauth]"
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
    base_url='http://localhost:5000',
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
    base_url='http://localhost:5000/auth',
    secret_key=app.config['SECRET_KEY']
)
AuthExtension(app, manager)

# El blueprint de /auth ya está registrado y listo para usarse.
```

### Configuración de Seguridad Personalizada
El módulo permite adaptar las reglas de contraseñas y sus mensajes de error fácilmente mediante clases de configuración anidadas.

```python
from auth_module.core.security.password import PasswordPolicy, PasswordPolicyConfig
from auth_module.core.security.rules import LengthPasswordRule, RegexPasswordRule
from auth_module.core.auth_manager import AuthManager

# 1. Definir las reglas y sus mensajes personalizados
config = PasswordPolicyConfig(
    rules=[
        LengthPasswordRule(
            value=12,
            message='La contraseña debe tener al menos {value} caracteres.'
        ),
        RegexPasswordRule(
            pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$',
            message='Debe incluir mayúsculas, minúsculas y números.'
        )
    ],
    msg_valid='Contraseña aceptada.'
)

# 2. (Opcional) Crear tus propias reglas
# Puedes extender PasswordRule; cualquier atributo que definas estará
# disponible automáticamente para formatear el 'message' o la traducción.
class MiReglaAvanzada(PasswordRule):
    palabra: str = 'admin'

    def validate(self, password: str) -> tuple[bool, str]:
        if self.palabra in password.lower():
            return False, 'La contraseña no puede contener la palabra {palabra}.'
        return True, ''

# 3. Instanciar la política
mi_politica = PasswordPolicy(config)

# 3. Inyectar la política en el AuthManager
manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='secreto',
    password_policy=mi_politica
)
```

---

### Prompt de Integración para Agentes (AI)
El siguiente bloque de texto está diseñado para que un agente de IA pueda comprender rápidamente la arquitectura del módulo y cómo integrarlo en tu proyecto. 

**Recomendación:** Asegúrate de que el agente al cual le des esta instrucción tenga en el *scope* de su contexto acceso al código fuente de este módulo y al código del proyecto donde va a ser integrado. Luego, envíale un prompt inicial similar a este:

> "Usando estrictamente la documentación provista, integra la biblioteca del módulo de autenticación 'auth-module' en mi proyecto. *(Añade aquí tus detalles: si quieres solo el core o también la interfaz gráfica, a dónde redirigir luego del login, dónde y cómo almacenar los usuarios, idioma, etc.)*"

Y a continuación, adjúntale este bloque de contexto técnico:

```text
Integra el Módulo de Autenticación en una aplicación Python para una gestión de usuarios robusta y agnóstica de frameworks.

## APIs del Módulo Disponibles

### Autenticación Core (auth_module.core.auth_manager)
- AuthManager: Orquestador principal. Métodos: `register_user(email, password)`, `authenticate_user(email, password)`, `verify_user(token)`, `request_password_recovery(email)`, `reset_password(email, password)`.
- TokenManager: Genera y verifica JWT seguros para validación de correo y recuperación.

### Seguridad y Políticas (auth_module.core.security)
- PasswordPolicyConfig: Agrupa reglas y mensajes de error mediante `rules=[]`.
- Reglas: `LengthRule(value, message)`, `RegexRule(pattern, message)`, o hereda de `AbsPasswordRule` para lógica personalizada.
- PasswordHasher: Utiliza `WerkzeugPasswordHasher` por defecto (scrypt).

### Despacho de Correos (auth_module.core.mail)
- MailBase: Interfaz abstracta para enviar correos.
- ConsoleMailDispatcher: Para desarrollo local. Imprime los correos en consola.
- SmtpMailDispatcher: Para producción. Conecta a servidores SMTP reales.

### Extensión de Flask (auth_module.flask_ext)
- AuthExtension(app, manager): Registra automáticamente blueprints, manejadores de error y plantillas.
- @login_required: Decorador para proteger rutas de Flask.
- set_login_redirect(endpoint): Configura la redirección post-login.

### Internacionalización y Mensajes (auth_module.core.i18n)
- I18nManager: Gestiona todos los textos de la interfaz y errores.
- Personalización: Configura el idioma nativo pasando `locale='es'` o `'en'`, y sobrescribe cualquier texto del sistema inyectando tu propio diccionario en el parámetro `custom_translations` durante la inicialización.

## Inicialización
La lógica core requiere inyección de dependencias. Debes proveer un despachador de correos, un repositorio de usuarios y variables de configuración (como secret_key y base_url).

## Ejemplo: Uso del Backend Core (Python)
from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.console_dispatcher import ConsoleMailDispatcher

repo = SQLiteUserRepository(db_path='./users.db')
mail = ConsoleMailDispatcher()
auth_manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='tu_secreto'
)
auth_manager.register_user('user@example.com', 'PassSeguro123!')

## Ejemplo: Integración con Flask
from flask import Flask
from auth_module.flask_ext.extension import AuthExtension
from auth_module.flask_ext.decorators import login_required

app = Flask(__name__)
# ... inicializar auth_manager ...
AuthExtension(app, auth_manager)

@app.route('/protegido')
@login_required
def protegido():
    return "Ruta protegida"

## Cuándo usar Core vs Extensión de Flask
- Core: Estás construyendo una app en FastAPI, Django, o CLI y solo necesitas la lógica de negocio.
- Extensión Flask: Estás construyendo una app en Flask y quieres rutas listas para usar (/auth/login, /auth/register) y plantillas HTML.

## Variables de Entorno (Para Correo SMTP)
- MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, NAME_SENDER, MAIL_SENDER_ADDRESS

## Documentación Detallada
- Core: auth_module/core/README.md
- Seguridad: auth_module/core/security/README.md
- Correo: auth_module/core/mail/README.md
- Flask: auth_module/flask_ext/README.md
```

---

## Internacionalización (i18n)

El módulo soporta traducción y localización tanto para el backend (mensajes de excepción, políticas de contraseña, correos electrónicos) como para el frontend (vistas, mensajes flash, formularios HTML) de forma completamente independiente y desacoplada.

Para entender a fondo su arquitectura y cómo el sistema encapsula los diccionarios base, ver la [Documentación de i18n](src/auth_module/core/i18n/README.md).

Por defecto, **el idioma principal es el español (`es`)**, y se configuran de forma separada en sus correspondientes puntos de inicialización:

### 1. Configuración del Core (Backend)
Al instanciar `AuthManager`, puedes definir el idioma del backend (`locale`) y/o pasar un diccionario de traducciones personalizadas (`custom_translations`):

```python
auth_manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='mi_secreto',
    locale='es',                      # Idioma del backend ('es' o 'en', por defecto 'es')
    custom_translations={             # Sobrescribir o añadir traducciones backend
        'es': {
            'user_exists': '¡Esta dirección de correo ya está en uso!'
        }
    }
)
```
También es posible pasar una función (*callable*) en `locale` para resolver el idioma del backend de manera dinámica en cada petición.

### 2. Configuración en la Extensión de Flask (Frontend)
Al instanciar `AuthExtension`, puedes configurar el idioma del frontend (`locale`) y sus traducciones de manera independiente, o controlarlo mediante la configuración de la app de Flask:

```python
# Configuración mediante la inicialización de la extensión
AuthExtension(
    app,
    auth_manager,
    locale='es',                      # Idioma del frontend ('es' o 'en', por defecto 'es')
    custom_translations={             # Sobrescribir o añadir traducciones frontend
        'es': {
            'email': 'Dirección de correo'
        }
    }
)
```

También es posible sobrescribir o definir estos valores de manera global a través de `app.config` de Flask:
```python
app = Flask(__name__)
app.config['AUTH_BACKEND_LOCALE'] = 'es'   # Sobrescribe el idioma del Core
app.config['AUTH_FRONTEND_LOCALE'] = 'en'  # Sobrescribe el idioma de las plantillas y mensajes flash
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

El proyecto cuenta con pruebas automáticas bajo la carpeta [tests/](tests). Para correrlas todas, primero debes instalar las dependencias de desarrollo (definidas en el grupo `dev` en `pyproject.toml` según el estándar [PEP 735](https://peps.python.org/pep-0735/)):

Si usas **uv**:
```bash
uv sync --group dev
```

Si usas **pip** (requiere `pip >= 25.1`):
```bash
pip install -e ./libs/auth-module --group dev
```
*(Nota: Si tu versión de pip es menor a la 25.1, puedes actualizarla con `pip install --upgrade pip`).*

Luego, ejecuta pytest:
```bash
pytest libs/auth-module/tests/
```
