from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError, \
    Email, Length, EqualTo, Regexp
from app.models import Users


class ForgotForm(FlaskForm):
    """
    Form for users to reset password
    """
    email = EmailField(
        'Email', 
        validators=[
            DataRequired(),
            Email(),
            Length(max=80)
        ]
    )


class SignInForm(FlaskForm):
    """
    Form for users to login
    """
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[A-Za-z0-9]+(?:[._][A-Za-z0-9]+)*$',
                message='Username must contain only letters numbers or underscore.'
            ),
            Length(min=4, max=32)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, max=32)
        ]
        )
    remember = BooleanField(
        'Remember Me'
        )


class SignupForm(FlaskForm):
    """
    Form for users to signup
    """
    email = EmailField(
        'Email', 
        validators=[
            DataRequired(),
            Email(),
            Length(max=80)
        ]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[A-Za-z0-9]+(?:[._][A-Za-z0-9]+)*$',
                message='Username must contain only letters numbers or underscore.'
            ),
            Length(min=4, max=32)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, max=32),
            EqualTo('confirm', message='Password doesn\'t match')
        ]
    )
    confirm = PasswordField(
        'Confirm Password'
    )
    accept_tos = BooleanField(
        'I accept the term of services',
        validators=[DataRequired()]
    )

    @staticmethod
    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('The email is already registered.')

    @staticmethod
    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already registered.')
