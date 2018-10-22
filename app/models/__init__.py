from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, \
    check_password_hash
from _datetime import datetime


class Users(UserMixin, db.Model):
    """
    Create an Users table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    isActive = db.Column(db.Boolean, nullable=False, index=True)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password = db.Column(db.String(80), nullable=False, index=True)

    def __init__(self, isActive, username, email, password):
        self.isActive = isActive
        self.username = username
        self.email = email
        self.password = self.gen_password(password)

    def __repr__(self):
        return '<User: {}, {}>'.format(self.username, self.email)

    @staticmethod
    def gen_password(password):
        return generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Set up user_loader
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Devices(UserMixin, db.Model):
    """
    Create a Devices table
    """

    __tablename__ = 'devices'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    host = db.Column(db.String(39), nullable=False, unique=True)
    port = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    device_status = db.relationship('DeviceStatus', uselist=False, backref="devices", lazy=True)

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.device_status = DeviceStatus()

    def __repr__(self):
        return '<Device: {}:{} | {}>'.format(self.host, self.port, self.device_status.status)


class DeviceStatus(UserMixin, db.Model):
    """
    Create a Device Status table
    that child from Devices
    """

    __tablename__ = 'device_status'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    status = db.Column(db.Boolean, nullable=False, default=False)
    checked_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self):
        self.status = False

    def __repr__(self):
        return '<Device Status: {}:{}>'.format(self.device_id, self.status)
