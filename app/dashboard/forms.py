from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, ValidationError, \
    Length, Regexp, NumberRange
from app.models import Devices


class add_device_form(FlaskForm):
    """
    Form for users to add new netconf device connection
    """
    host = StringField(
        'Host',
        validators=[
            DataRequired(),
            Regexp(r'(^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$)|(^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$)', message='Invalid hostname or IPv4 address.')]
    )
    port = IntegerField(
        'Port',
        validators=[DataRequired(), NumberRange(min=1, max=65535)]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(r'^[A-Za-z0-9]+(?:[._][A-Za-z0-9]+)*$', message='Username must contain only letters, numbers or underscore.'),
            Length(max=32)]
        )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=3, max=32)]
        )

    @staticmethod
    def validate_host(self, field):
        if Devices.query.filter_by(host=field.data).first():
            raise ValidationError('The host has already existed.')
