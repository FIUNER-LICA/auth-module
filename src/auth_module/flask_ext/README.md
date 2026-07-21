# Documentación de la Extensión de Flask (`flask_ext`)

Este subpaquete toma la lógica independiente del `AuthManager` y provee una integración completa, lista para usarse, dentro del framework Flask.

## Inicialización (`extension.py`)
La integración principal se realiza mediante la clase `AuthExtension`. 
Al inicializarla, ésta registra automáticamente el **Blueprint de Autenticación** y los **Manejadores de Errores** necesarios.

```python
from auth_module.flask_ext.extension import AuthExtension

# manager = AuthManager(...)
AuthExtension(app, manager)
```

## Rutas Automáticas
El Blueprint monta automáticamente los siguientes endpoints bajo el prefijo `/auth`:
- `/auth/register`
- `/auth/login`
- `/auth/logout`
- `/auth/verify/<token>`
- `/auth/password-recovery`
- `/auth/reset-password/<token>`

## Control de Acceso (`decorators.py`)
Para proteger tus propias rutas de Flask, la extensión expone decoradores nativos:

```python
from auth_module.flask_ext.decorators import login_required

@app.route('/dashboard')
@login_required
def dashboard():
    return "Bienvenido a tu panel protegido."
```
*(El decorador automáticamente redirigirá al usuario a `/auth/login` si no está autenticado).*

### Redirección Personalizada
Si deseas que, después de hacer login exitoso, el usuario sea redirigido a una página distinta en lugar del `/` por defecto, puedes configurarlo:

```python
from auth_module.flask_ext.extension import set_login_redirect

set_login_redirect('/mi-dashboard')
```

## Interfaz Gráfica (`templates/`)
La extensión incluye todas las plantillas HTML renderizadas con Jinja2. Las pantallas de inicio de sesión, registro y notificaciones flash ya tienen estilos CSS integrados. Todo el código base y los identificadores están en inglés, mientras que los textos renderizados para el usuario están en español.
