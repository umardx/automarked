from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, \
    check_password_hash
from _datetime import datetime, timezone
import socket


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
        return '<user={},{}>'.format(self.username, self.email)

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
        self.update_status()

    def __repr__(self):
        return '<device:{}:{}>'.format(self.host, self.port)

    def update(self, port, username, password):
        self.port = port
        self.username = username
        self.password = password
        self.update_status()

    def update_status(self):
        self.device_status = DeviceStatus(self.host, self.port)


class DeviceStatus(UserMixin, db.Model):
    """
    Create a Device Status table
    that child from Devices
    """

    __tablename__ = 'device_status'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    status = db.Column(db.Boolean, nullable=False, default=False)
    checked_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, host, port):
        self.status = self.is_open(host, port)
        self.checked_time = datetime.now(timezone.utc)

    def __repr__(self):
        return '<status:{}:{}>'.format(self.device_id, self.status)

    @staticmethod
    def is_open(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((host, port))
            sock.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False
        finally:
            sock.close()
