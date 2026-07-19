"""
Flask Extension
===============

This package contains the optional Flask integration for auth-module,
including blueprints, routes, templates, and view controllers.
"""

from .extension import AuthExtension
from .decorators import login_required
from .routes import set_login_redirect

__all__ = ['AuthExtension', 'login_required', 'set_login_redirect']
