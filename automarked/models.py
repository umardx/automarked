from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Email, Length, EqualTo
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

class SignupForm(FlaskForm):
    email = EmailField(
        'Email', 
        validators=[InputRequired(), 
        Email(message='Invalid email'), 
        Length(max=80)]
        )
    username = StringField(
        'Username',
        validators=[InputRequired(),
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

class err_msg(object):
    def __init__(self, title, message, category):
        self.title = title
        self.message = message
        self.category = category

db.create_all()
db.session.commit()
