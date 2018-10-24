from app import celery
from app.models import Devices
from app import db
from time import sleep


@celery.task
def reverse(msg):
    return msg[::-1]


@celery.task
def reverse_ten(msg):
    sleep(12)
    return msg[::-1]


@celery.task
def wait_sec(second):
    sleep(second)
    return True


@celery.task
def refresh_all_device(user_id):
    devices = Devices.query.filter_by(
        user_id=user_id
    ).all()
    for _device in devices:
        _device.update_status()

    try:
        db.session.commit()
        return True
    except:
        return False
