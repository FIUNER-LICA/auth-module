# Core Documentation

The `core/` directory contains all the framework-agnostic business logic of the Authentication Module. This means that no class in this package depends on a web framework (like Flask or Django).

## Main Components

### 1. AuthManager (`auth_manager.py`)
It is the main orchestrator. It uses Dependency Injection to interact with the database, the password manager, and the email service.

```python
manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='secret',
    backend_locale='es',              # Optional: backend locale ('es' or 'en', defaults to 'es')
    frontend_locale='es',             # Optional: frontend locale ('es' or 'en', defaults to 'es')
    custom_translations=None          # Optional: dictionary to override translations
)
```
Provides ready-to-use methods such as:
- `register_user(email, password)`
- `authenticate_user(email, password)`
- `verify_user(token)`
- `request_password_recovery(email)`

### 2. Database (`db/`)
Defines the `UserRepository` interface which ensures that any database implementation will expose the necessary methods (`create_user`, `get_user_by_email`, etc.).
A default implementation is provided: `SQLiteUserRepository`, ideal for rapid deployment without complex infrastructure.

### 3. Token Manager (`tokens.py`)
Uses `itsdangerous` for the secure generation of JWT tokens used in:
- Email verification.
- Password recovery.
The tokens are encrypted and have an expiration time.
