from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from automarked import db

class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
        )
    username = db.Column(
        db.String(20),
        unique=True
        )
    email = db.Column(
        db.String(80),
        unique=True
        )
    password = db.Column(
        db.String(100)
        )

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired(),
        Length(min=4, max=20)
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
        Length(min=4, max=20)]
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

db.create_all()
db.session.commit()