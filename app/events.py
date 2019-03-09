import functools
from app import socket_io, tasks
from app.models import YangModel
from flask import request, url_for
from flask_login import current_user
from flask_socketio import disconnect, emit


clients = []


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@socket_io.on('connect', namespace='/nc')
@authenticated_only
def on_connect():
    clients.append(request.sid)
    emit_data = {
        'session': '{}'.format(request.sid),
        'connected': True
    }
    emit('receive', emit_data, room=request.sid)
    print('Client connected {}'.format(clients))


@socket_io.on('render_req', namespace='/nc')
@authenticated_only
def render_req(message):
    if message:
        _ym = YangModel(
            operation=message.get('operation'),
            key_model=message.get('model')
        )
        emit_data = _ym.get_data_model()
    else:
        emit_data = {}
    emit('render_req', emit_data, room=request.sid)


@socket_io.on('render_res', namespace='/nc')
@authenticated_only
def render_res(message):
    url = 'http://webapp:8000/dashboard/netconf/emit'
    data = message.get('data')
    tasks.netconf.delay(data, request.sid, url)


@socket_io.on('disconnect', namespace='/nc')
def on_disconnect():
    clients.remove(request.sid)
    print('Client disconnected {}'.format(clients))
