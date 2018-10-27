from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required

from app.dashboard import dashboard
from app.dashboard.forms import add_device_form
from app import db
from app.models import Devices


@dashboard.route('/')
@login_required
def index():
    """
    Handle requests to the /dashboard/ route
    Show dashboard display
    """
    
    return render_template('dashboard/index.html', title='Dashboard')


@dashboard.route('/add_device', methods=['GET', 'POST'])
@login_required
def add_device():
    """
    Handle requests to the /dashboard/add_device route
    User can add netconf device
    """
    form_add_device = add_device_form()

    if request.method == 'POST' and form_add_device.validate_on_submit():
        _device = Devices(
            host=form_add_device.host.data,
            port=form_add_device.port.data,
            username=form_add_device.username.data,
            password=form_add_device.password.data
        )

        try:
            db.session.add(_device)
            db.session.commit()
            flash(u'The device was successfully added.', 'success')
        except Exception as e:
            flash(u'Can\'t add device to the database. ' + str(e), 'error')

    return render_template('dashboard/add_device.html', title='Add Device | Dashboard', form_add_device=form_add_device)


@dashboard.route('/list_device', methods=['GET', 'POST'])
@login_required
def list_device():
    """
    Handle requests to the /dashboard/list_device route
    User can list netconf device
    moment('2018-10-22 11:03:24.422888','YYYY-MM-DD hh:mm:ss.SSSSSS').fromNow();
    """

    devices = Devices.query.all()
    return render_template('dashboard/list_device.html', title='List Device | Dashboard', devices=devices)


@dashboard.route('/check_status/<int:device_id>')
@login_required
def check_status(device_id):
    _device = Devices.query.filter_by(id=device_id).first()
    _device.update_status()
    try:
        db.session.commit()
        flash(u'The device was successfully refresh the device.', 'success')
    except Exception as e:
        flash(u'Can\'t add device to the database. ' + str(e), 'error')
    return redirect(url_for('dashboard.list_device'))


@dashboard.route('/delete_device/<int:device_id>')
@login_required
def delete_device(device_id):
    _device = Devices.query.filter_by(id=device_id).first()

    try:
        db.session.delete(_device)
        db.session.commit()
        flash(u'You were successfully deleted device', 'success')
    except Exception as e:
        flash(u'Can\'t delete device.' + str(e), 'error')

    return redirect(url_for('dashboard.list_device'))
