from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import InputRequired, DataRequired, \
    Email, Length, EqualTo, Regexp, IPAddress, HostnameValidation, \
    NumberRange
from automarked import db

class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer,
        nullable=False,
        primary_key=True
        )
    isActive = db.Column(
        db.Boolean,
        nullable=False
    )
    username = db.Column(
        db.String(32),
        nullable=False,
        unique=True
        )
    email = db.Column(
        db.String(80),
        nullable=False,
        unique=True
        )
    password = db.Column(
        db.String(80),
        nullable=False
        )


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired(),
        Regexp(r'^[A-Za-z0-9]+(?:[._][A-Za-z0-9]+)*$', message='Username must contain only letters numbers or underscore.'),
        Length(min=4, max=32)
        ])
    password = PasswordField(
        'Password',
        validators=[InputRequired(),
        Length(min=6, max=32)]
        )
    remember = BooleanField(
        'Remember Me'
        )

class ForgotEmailForm(FlaskForm):
    email = EmailField(
        'Email', 
        validators=[InputRequired(), 
        Email(), 
        Length(max=80)]
        )

class ForgotPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[InputRequired(), 
        Length(min=6, max=32),
        EqualTo('confirm', message='Password doesn\'t match.')]
        )
    confirm = PasswordField(
        'Confirm Password'
    )

class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[InputRequired(), 
        Length(min=6, max=32, message="Password must be betwen 6 and 32 characters long."),
        EqualTo('confirm', message='Password doesn\'t match')]
        )
    confirm = PasswordField(
        'Confirm Password'
    )

class SignupForm(FlaskForm):
    email = EmailField(
        'Email', 
        validators=[InputRequired(), 
        Email(), 
        Length(max=80)]
        )
    username = StringField(
        'Username',
        validators=[InputRequired(),
        Regexp(r'^[A-Za-z0-9]+(?:[._][A-Za-z0-9]+)*$', message='Username must contain only letters numbers or underscore.'),
        Length(min=4, max=32)]
        )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), 
        Length(min=6, max=32),
        EqualTo('confirm', message='Password doesn\'t match')]
        )
    confirm = PasswordField(
        'Confirm Password'
    )
    accept_tos = BooleanField(
        'I accept the term of services',
        validators=[DataRequired()]
    )

class AddDeviceForm(FlaskForm):
    host = StringField(
        'Host',
        validators=[DataRequired(), HostnameValidation(allow_ip=True), IPAddress(ipv6=True)],
    )
    port = IntegerField(
        'Port',
        validators=[DataRequired(), NumberRange(min=1, max=65535)]
    )
    username = StringField(
        'Username',
        validators=[DataRequired(),
        Regexp(r'^[A-Za-z0-9]+(?:[._][A-Za-z0-9]+)*$', message='Username must contain only letters numbers or underscore.'),
        Length(max=32)]
        )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), 
        Length(max=32)]
        )

db.create_all()
db.session.commit()
