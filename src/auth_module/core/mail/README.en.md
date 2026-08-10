# Mail Documentation

The mail package handles all outgoing communication with the user (account verification and password recovery).

## Abstract Interface (`base.py`)
All mail dispatching classes implement the abstract `MailDispatcher` class, which requires the `send(to_email, subject, body)` method. 
This allows swapping providers (SendGrid, AWS SES, SMTP, Console) without modifying the `AuthManager` logic.

## Included Dispatchers

### 1. ConsoleMailDispatcher (`console_dispatcher.py`)
**Ideal for local development.**
This dispatcher intercepts the email and prints it in a readable format to the terminal. It does not require configuring SMTP servers or environment variables. 
It allows you to directly click on the validation and recovery links that appear in the console.

### 2. SmtpMailDispatcher (`smtp_dispatcher.py`)
**Ideal for production environments.**
Sends actual emails using an SMTP server. 
It is configured via the `EmailEnvConfig` class, which expects the following environment variables:
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `NAME_SENDER`
- `MAIL_SENDER_ADDRESS`

**Usage:**
```python
from auth_module.core.mail.config import EmailEnvConfig
from auth_module.core.mail.smtp_dispatcher import SmtpMailDispatcher

# Will automatically load values from the system/.env file
config = EmailEnvConfig()
mail = SmtpMailDispatcher(config)
```
