"""
WTForms for the authentication module.
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    """Form for user registration."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repassword = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='passwords_not_match')]
    )
    submit = SubmitField('Register')


class PasswordRecoveryForm(FlaskForm):
    """Form for requesting a password reset link."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Recover Password')


class PasswordResetForm(FlaskForm):
    """Form for resetting the password with a token."""
    password = PasswordField('New Password', validators=[DataRequired()])
    repassword = PasswordField(
        'Confirm New Password',
        validators=[DataRequired(), EqualTo('password', message='passwords_not_match')]
    )
    submit = SubmitField('Reset Password')
