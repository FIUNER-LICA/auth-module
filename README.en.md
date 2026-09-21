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

Since this package was designed as a modular library, the most practical way to integrate it into your project is to install it directly from GitHub via `pip`, referencing the [latest stable version](https://github.com/FIUNER-LICA/auth-module/releases/latest).

### Install with pip
Activate your main project's virtual environment and install the module according to your needs.

Basic Installation (Core Only, no Flask) of version "v1.1.0":
```bash
pip install git+https://github.com/FIUNER-LICA/auth-module.git@v1.1.0
```

Flask Installation (Includes web dependencies and views):
```bash
pip install "git+https://github.com/FIUNER-LICA/auth-module.git@v1.1.0[flask]"
```

Complete Installation (Includes optional dependencies like Flask and OAuth):
```bash
pip install "git+https://github.com/FIUNER-LICA/auth-module.git@v1.1.0[flask,oauth]"
```

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
from auth_module.flask_ext.extension import FlaskExtension
# ... import repo and mail_dispatcher ...

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'
app.config['SESSION_TYPE'] = 'filesystem'

# Configure the Manager and pass it to the Extension
manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000/auth',
    secret_key=app.config['SECRET_KEY']
)
FlaskExtension(app, manager)

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

---

### Agent Integration Prompt
The following text block is designed for an AI agent to quickly understand the module's architecture and how to integrate it into your project.

**Recommendation:** Ensure that the agent you give this instruction to has access to both this module's source code and your project's source code in its context *scope*. Then, send an initial prompt similar to this:

> "Using strictly the provided documentation, integrate the authentication module library 'auth-module' into my project. *(Add your specific details here: whether you want just the core or the GUI as well, where to redirect after login, where and how to store users, language, etc.)*"

And immediately after, attach this technical context block:

```text
Integrate Authentication Module into a Python application for robust, framework-agnostic user management.

## Available Module APIs

### Core Authentication (auth_module.core.auth_manager)
- AuthManager: Main orchestrator. Methods: `register_user(email, password)`, `authenticate_user(email, password)`, `verify_user(token)`, `request_password_recovery(email)`, `reset_password(email, password)`.
- TokenManager: Generates and verifies secure JWT tokens for email verification and recovery.

### Security & Policies (auth_module.core.security)
- PasswordPolicyConfig: Group constraints and error messages using `rules=[]`.
- Rules: `LengthRule(value, message)`, `RegexRule(pattern, message)`, or inherit from `AbsPasswordRule` for custom logic.
- PasswordHasher: Uses `WerkzeugPasswordHasher` by default (scrypt).

### Mail Dispatching (auth_module.core.mail)
- MailBase: Abstract interface for sending emails.
- ConsoleMailDispatcher: For local development. Prints emails to stdout.
- SmtpMailDispatcher: For production. Connects to real SMTP servers.

### Flask Extension (auth_module.flask_ext)
- FlaskExtension(app, manager, login_redirect_endpoint): Automatically registers blueprints, error handlers, templates and configures post-login redirection.
- @login_required: Decorator to protect Flask routes.

### Internationalization & Messages (auth_module.core.i18n)
- I18nManager: Manages all UI and error texts.
- Customization: Set the native language by passing `locale='es'` or `'en'`, and override any system text by injecting your own dictionary into the `custom_translations` parameter during initialization.

## Initialization
The core logic requires dependency injection. You must provide a mail dispatcher, a user repository, and configuration variables (like secret_key and base_url).

## Example: Core Backend Usage (Python)
from auth_module.core.auth_manager import AuthManager
from auth_module.core.db.sqlite_repository import SQLiteUserRepository
from auth_module.core.mail.console_dispatcher import ConsoleMailDispatcher

repo = SQLiteUserRepository(db_path='./users.db')
mail = ConsoleMailDispatcher()
auth_manager = AuthManager(
    mail_dispatcher=mail,
    user_repository=repo,
    base_url='http://localhost:5000',
    secret_key='your_secret_key'
)
auth_manager.register_user('user@example.com', 'SecurePass123!')

## Example: Flask Integration
from flask import Flask
from auth_module.flask_ext.extension import FlaskExtension
from auth_module.flask_ext.decorators import login_required

app = Flask(__name__)
# ... initialize auth_manager ...
FlaskExtension(app, auth_manager)

@app.route('/protected')
@login_required
def protected():
    return "This is protected"

## When to Use Core vs Flask Extension
- Core: You are building a FastAPI, Django, or CLI application and only need the business logic.
- Flask Extension: You are building a Flask app and want ready-to-use routes (/auth/login, /auth/register) and HTML templates.

## Environment Variables (For SMTP Mail)
- MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, NAME_SENDER, MAIL_SENDER_ADDRESS

## Detailed Documentation
- Core: auth_module/core/README.en.md
- Security: auth_module/core/security/README.en.md
- Mail: auth_module/core/mail/README.en.md
- Flask: auth_module/flask_ext/README.en.md
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
When instantiating `FlaskExtension`, you can configure the frontend language (`locale`) and its translations independently, or control them via the Flask app configuration:

```python
# Configuration via extension initialization
FlaskExtension(
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

If using **uv**, you can sync all dependencies (including optional extras and development tools) by running:
```bash
uv sync --all-extras
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
