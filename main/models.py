from flask_login import UserMixin
from main import db, login_manager
from flask import render_template
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, \
    check_password_hash
from _datetime import datetime, timezone
from humanize import naturaltime
from socket import error as socket_error
import socket
import json

from ydk.services import NetconfService
from ydk.services import Datastore
from ydk.providers import NetconfServiceProvider

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider

json_provider = CodecServiceProvider(type='json')
xml_provider = CodecServiceProvider(type='xml')
codec = CodecService()
nc = NetconfService()


class Users(UserMixin, db.Model):
    """
    Create an Users table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    mark_active = db.Column(db.Boolean, nullable=False, index=True)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password = db.Column(db.String(80), nullable=False, index=True)
    notifications = db.relationship('Notification', backref='users', lazy='dynamic')
    tasks = db.relationship('Task', backref='users', lazy='dynamic')

    def __init__(self, mark_active, username, email, password):
        self.mark_active = mark_active
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

    def get_unread_notifs(self, reverse=False):
        notifications = []
        unread_notifications = Notification.query.filter_by(user_id=self.id, mark_read=False)

        for notification in unread_notifications:
            notifications.append({
                'id': notification.id,
                'title': notification.title,
                'category': notification.category,
                'message': notification.message,
                'received': naturaltime(datetime.now() - notification.received_at),
                'mark_read': notification.mark_read
            })

        if reverse:
            return list(reversed(notifications))
        else:
            return notifications


# Set up user_loader
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Notification(UserMixin, db.Model):
    """
    Create a Notification table
    """

    __tablename__ = 'notifications'

    id = db.Column(db.Integer,  nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mark_read = db.Column(db.Boolean, nullable=False, default=False)
    received = db.Column(db.DateTime, nullable=False, index=True, default=datetime.now())
    title = db.Column(db.String(128), nullable=False, index=True)
    category = db.Column(db.SmallInteger, nullable=False, index=True)
    message = db.Column(db.Text)

    def __repr__(self):
        return '<{}-{}:{}>'.format(self.received, self.title, self.message)


class Task(UserMixin, db.Model):
    """
    Create a Task table
    """

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.String(128), nullable=False)
    received = db.Column(db.DateTime, nullable=False, index=True, default=datetime.now())
    title = db.Column(db.String(128), nullable=False, index=True)
    category = db.Column(db.SmallInteger, nullable=False, index=True)
    progress = db.Column(db.SmallInteger, nullable=False, default=0)

    def __repr__(self):
        return '<{}:{}>'.format(self.task_id, self.progress)


class Devices(UserMixin, db.Model):
    """
    Create a Devices table
    """

    __tablename__ = 'devices'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    host = db.Column(db.String(39), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    device_status = db.relationship('DeviceStatus', uselist=False, backref="devices", lazy=True)

    @login_required
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.user_id = current_user.id
        self.create_status()

    def __repr__(self):
        return '<device:{}:{}>'.format(self.host, self.port)

    def update(self, port, username, password):
        self.port = port
        self.username = username
        self.password = password
        self.create_status()

    def create_status(self):
        self.device_status = DeviceStatus(self.host, self.port)

    def update_status(self):
        self.device_status.update(self.host, self.port)


class DeviceStatus(UserMixin, db.Model):
    """
    Create a Device Status table
    that child from Devices
    """

    __tablename__ = 'device_status'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    status = db.Column(db.Boolean, nullable=False, default=False)
    checked_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, host, port):
        self.status = self.is_open(host, port)
        self.checked_time = datetime.now(timezone.utc)

    def __repr__(self):
        return '<status:{}:{}>'.format(self.device_id, self.status)

    def update(self, host, port):
        self.status = self.is_open(host, port)
        self.checked_time = datetime.now(timezone.utc)

    @staticmethod
    def is_open(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((host, port))
            sock.shutdown(socket.SHUT_RDWR)
            return True
        except (Exception, socket_error):
            return False
        finally:
            sock.close()


class NetConf:
    def __init__(self, address, port, username, password):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.session = self.create_session()

    def create_session(self):
        return NetconfServiceProvider(
            address=self.address,
            port=self.port,
            username=self.username,
            password=self.password
        )

    # Retrieve running configuration and device state information.
    def get(self, read_filter=[]):
        return nc.get(provider=self.session, read_filter=read_filter)

    # Retrieve all or part of a specified configuration datastore.
    def get_config(self, source=Datastore.candidate, read_filter=[]):
        return nc.get_config(provider=self.session, source=source, read_filter=read_filter)

    # Loads all or part of a specified configuration to the specified target configuration datastore.
    # Allows new configuration to be read from local file, remote file, or inline.
    # If the target configuration datastore does not exist, it will be created.
    def edit_config(
            self, target=Datastore.candidate, config=[], default_operation='replace',
            test_option='rollback-on-error'
    ):
        return nc.edit_config(
            self.session, target=target, config=config,
            default_operation=default_operation,
            test_option=test_option
        )

    # Delete a configuration Datastore. The RUNNING configuration Datastore cannot be deleted.
    def delete_config(self, target=Datastore.candidate, url=''):
        return nc.delete_config(provider=self.session, target=target, url=url)

    # Method for return supported operations
    @staticmethod
    def support_operations():
        operations = {
            'get-config': '<get-config>',
            'edit-config': '<edit-config>'
        }
        return operations


class YangModel:
    def __init__(self, key_model, operation):
        self.operation = operation
        if key_model in self.support_models().keys():
            self.model = key_model
        else:
            self.model = None

    @staticmethod
    def support_models():
        models = {
            'manual': 'Input-Manually',
            'ifmgr-cfg': 'Cisco-IOS-XR-ifmgr-cfg',
            'ipv4-ospf-cfg': 'Cisco-IOS-XR-ipv4-ospf-cfg',
            'ipv6-ospfv3-cfg': 'Cisco-IOS-XR-ipv6-ospfv3-cfg',
            'telemetry-model-driven-cfg': 'Cisco-IOS-XR-telemetry-model-driven-cfg'
        }
        return models

    def get_data_model(self):
        if self.model is not None and self.model != 'manual':
            _path = 'data-models/{}/{}.json'.format(self.operation, self.model)
            data_model = json.loads(render_template(_path))
            return data_model
        else:
            return {
                "<module-name>:<container-name>": {
                    "<leaf-name>": []
                }
            }
