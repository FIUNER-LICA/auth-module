# Authentication Module

A robust, framework-agnostic, and highly modular authentication system designed to be consumed as an installable Python package.

The module provides a solid foundation (Core) that handles all password validation logic, secure hashing, database interaction (SQLite), and email dispatching. Additionally, it includes a comprehensive and optional Flask extension that brings ready-to-use routes and templates.

## Key Features

- Agnostic by Design: All core business logic ([AuthManager](src/auth_module/core/auth_manager.py)) is independent of any web framework.
- Flask Extension: Pre-configured blueprints and templates for user registration, login, and password recovery in the [flask_ext](src/auth_module/flask_ext) directory.
- Configurable Security: Injectable password policies and adaptive hashing support in the [security](src/auth_module/core/security) directory.
- Swappable Mail Dispatcher: Various adapters available, such as pure SMTP or a console-based dispatcher for local development in the [mail](src/auth_module/core/mail) directory.

---

## Installation and Usage in External Projects

Since this package was designed as a library, the best way to integrate it into your project is through `pip`, treating it as a local dependency.

### 1. Clone the repository
Clone this repository into your main project directory (for example, inside a folder called `libs/` or `deps/`).

```bash
mkdir libs
cd libs
git clone <url-to-this-repository> auth-module
```

### 2. Ignore the folder in your version control
It is highly important to add this folder to your main project's `.gitignore` to prevent accidentally tracking nested repositories.

Add this to your `.gitignore` file:
```text
# Ignore local dependencies
libs/auth-module/
# Or if you used deps:
# deps/auth-module/
```

### 3. Install with pip
Activate your main project's virtual environment and install the module.

Basic Installation (Core Only, no Flask):
```bash
pip install ./libs/auth-module
```

Flask Installation (Includes web dependencies and views):
```bash
pip install "./libs/auth-module[flask]"
```

Complete Installation (Includes optional dependencies like Flask and OAuth):
```bash
pip install "./libs/auth-module[flask,oauth]"
```

*(Note: Using the `-e` flag during `pip install` is useful if you plan on modifying the auth-module code and want to see the changes reflected instantly in your project).*

---

## Quick Start

The package includes an [examples/](examples) directory at the root of the project with ready-to-run code. Below are the key concepts:

### Pure Usage (Backend Only)
See the full example at: [examples/01_core_backend/main.py](examples/01_core_backend/main.py)

```python
from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.console_dispatcher import ConsoleMailDispatcher

# 1. Database
repo = SQLiteUserRepository(db_path='/absolute/path/users.db')

# 2. Mail Dispatcher (Console for dev)
mail = ConsoleMailDispatcher()

# 3. Main Manager
auth_manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='my_secret'
)

# Usage
auth_manager.register_user('hello@example.com', 'SecurePass123!')
```

### Flask Usage
See the full example at: [examples/02_flask_extension/app.py](examples/02_flask_extension/app.py)

```python
from flask import Flask
from auth_module.flask_ext.extension import AuthExtension
# ... import repo and mail_dispatcher ...

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'
app.config['SESSION_TYPE'] = 'filesystem'

# Configure the Manager and pass it to the Extension
manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key=app.config['SECRET_KEY']
)
AuthExtension(app, manager)

# The /auth blueprint is now registered and ready to use.
```

### Custom Security Configuration
The module allows you to easily adapt password rules and their error messages using nested configuration classes.

```python
from auth_module.core.security.password import PasswordPolicy, PasswordPolicyConfig
from auth_module.core.security.rules import LengthPasswordRule, RegexPasswordRule
from auth_module.core.auth_manager import AuthManager

# 1. Define rules and custom messages
config = PasswordPolicyConfig(
    rules=[
        LengthPasswordRule(
            value=12, 
            message='Password must be at least {value} characters long.'
        ),
        RegexPasswordRule(
            pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$',
            message='Must include uppercase, lowercase, and numbers.'
        )
    ],
    msg_valid='Password accepted.'
)

# 2. (Optional) Create your own custom rules
# You can extend PasswordRule; any attribute you define will be
# automatically available for formatting the 'message' or translation.
class MyAdvancedRule(PasswordRule):
    word: str = 'admin'

    def validate(self, password: str) -> tuple[bool, str]:
        if self.word in password.lower():
            return False, 'The password cannot contain the word {word}.'
        return True, ''

# 3. Instantiate the policy
my_policy = PasswordPolicy(config)

# 3. Inject the policy into the AuthManager
manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='secret',
    password_policy=my_policy
)
```


## Internationalization (i18n)

The module supports translation and localization for both the backend (exception messages, password policies, email dispatches) and the frontend (routes, flash messages, HTML forms) in a fully decoupled and independent manner.

To fully understand its architecture and how the system encapsulates base dictionaries, see the [i18n Documentation](src/auth_module/core/i18n/README.en.md).

By default, **the main language is Spanish (`es`)**, and they are configured separately in their respective initialization contexts:

### 1. Core (Backend) Configuration
When instantiating `AuthManager`, you can define the backend language (`locale`) and/or pass a custom translations dictionary (`custom_translations`):

```python
auth_manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='my_secret',
    locale='es',                      # Backend locale ('es' or 'en', defaults to 'es')
    custom_translations={             # Override or add backend translations
        'en': {
            'user_exists': 'This email is already registered.'
        }
    }
)
```
You can also pass a *callable* function in `locale` to resolve the backend language dynamically per request.

### 2. Flask Extension (Frontend) Configuration
When instantiating `AuthExtension`, you can configure the frontend language (`locale`) and its translations independently, or control them via the Flask app configuration:

```python
# Configuration via extension initialization
AuthExtension(
    app,
    auth_manager,
    locale='es',                      # Frontend locale ('es' or 'en', defaults to 'es')
    custom_translations={             # Override or add frontend translations
        'en': {
            'email': 'Email address'
        }
    }
)
```

You can also override or define these values globally in the Flask `app.config` object:
```python
app = Flask(__name__)
app.config['AUTH_BACKEND_LOCALE'] = 'es'   # Overrides the Core backend language
app.config['AUTH_FRONTEND_LOCALE'] = 'en'  # Overrides the templates and flash messages language
```

---

## Project Structure

- [src/auth_module/core/](src/auth_module/core): All foundational logic (Database, Hashing, Mail, Tokens).
- [src/auth_module/flask_ext/](src/auth_module/flask_ext): Flask integration (Routes, Decorators, Templates, Styles).
- [examples/](examples): Detailed implementation examples (Core backend, Flask extension, Custom security).
- [tests/](tests): Comprehensive modular unit test suite.
- [pyproject.toml](pyproject.toml): Package and dependency definitions.

---

## Testing

The project is fully covered by automated tests under the [tests/](tests) folder. To run them, you first need to install the development dependencies (defined in the `dev` group of `pyproject.toml` under the [PEP 735](https://peps.python.org/pep-0735/) standard):

If using **uv**:
```bash
uv sync --group dev
```

If using **pip** (requires `pip >= 25.1`):
```bash
pip install -e ./libs/auth-module --group dev
```
*(Note: If you have an older version of pip, you can upgrade it via `pip install --upgrade pip`).*

Then, run pytest:
```bash
pytest libs/auth-module/tests/
```
