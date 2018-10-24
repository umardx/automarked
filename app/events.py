from app import socket_io
from flask_socketio import send, emit


@socket_io.on('connect')
def when_connect():
    print('Client connected')


@socket_io.on('disconnect')
def when_disconnect():
    print('Client disconnected')


@socket_io.on('message')
def when_message(message):
    print('received message: ' + message)
