from flask import flash, redirect, url_for, \
    render_template, request, jsonify
from flask_login import login_required, current_user

from app.dashboard import dashboard
from app.dashboard.forms import add_device_form, edit_device_form
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

    return render_template(
        'dashboard/add_device.html',
        title='Add Device | Dashboard',
        form_add_device=form_add_device
    )


@dashboard.route('/list_device', methods=['GET', 'POST'])
@login_required
def list_device():
    """
    Handle requests to the /dashboard/list_device route
    User can list netconf device
    moment('2018-10-22 11:03:24.422888','YYYY-MM-DD hh:mm:ss.SSSSSS').fromNow();
    """
    form_edit_device = edit_device_form()

    if request.method == 'POST':
        _id = request.form['id']

        if form_edit_device.validate_on_submit():
            _device = Devices(
                host=form_edit_device.host.data,
                port=form_edit_device.port.data,
                username=form_edit_device.username.data,
                password=form_edit_device.password.data
            )

            edit(_device, _id)

        else:
            for field in form_edit_device.errors:
                _error = 'Field ' + str(field) + ': ' + str(
                    form_edit_device.errors[field])\
                    .replace("['", "").replace("']", "")

                flash(u'' + _error, 'warning')

            return redirect(url_for(
                'dashboard.list_device',
                device_id=_id
            ) + '#editDevice')

    devices = Devices.query.filter_by(user_id=current_user.id).all()

    action = request.args.get('action')
    device_id = request.args.get('device_id')

    if action == 'refresh':
        refresh(device_id)
    elif action == 'refresh_all':
        refresh_all(devices)
    elif action == 'delete':
        delete(device_id)
    elif action == 'telemetry':
        pass
    elif action == 'netconf':
        pass

    return render_template(
        'dashboard/list_device.html',
        title='List Device | Dashboard',
        form_edit_device=form_edit_device,
        devices=Devices.query.filter_by(
            user_id=current_user.id
        ).all(),
        device_id=device_id
    )


def refresh(id):
    _device = Devices.query.filter_by(id=id).first()
    _device.update_status()

    try:
        db.session.commit()
        flash(
            u'All devices were successfully refreshed.',
            'success'
        )
    except Exception as e:
        flash(u'Can\'t refresh the device. ' + str(e), 'error')
    return redirect(url_for('dashboard.list_device'))


def refresh_all(devices):
    for _device in devices:
        _device.update_status()

    try:
        db.session.commit()
        flash(u'The device was successfully refreshed.', 'success')
    except Exception as e:
        flash(u'Can\'t refresh the device. ' + str(e), 'error')
    return redirect(url_for('dashboard.list_device'))


def delete(id):
    _device = Devices.query.filter_by(id=id).first()

    try:
        db.session.delete(_device)
        db.session.commit()
        flash(u'You were successfully deleted the device.', 'success')
    except Exception as e:
        flash(u'Can\'t delete device. ' + str(e), 'error')

    return redirect(url_for('dashboard.list_device'))


def edit(device, id):
    try:
        _device = Devices.query.filter_by(id=id).first()
        _device.update(
            port=device.port,
            username=device.username,
            password=device.password
        )
        db.session.commit()
        flash(u'The device was successfully updated', 'success')
    except AttributeError as e:
        flash(u'Can\'t determine the device. ' + str(e), 'error')
    except Exception as e:
        flash(u'Can\'t update the device. ' + str(e), 'error')

    return redirect(url_for('dashboard.list_device'))


@dashboard.route('/device/<id>')
@login_required
def device(id):
    data = dict()
    _device = Devices.query.filter_by(id=id).first()
    if _device is not None:
        data['id'] = _device.id
        data['host'] = _device.host
        data['port'] = _device.port
        data['username'] = _device.username
        data['password'] = _device.password

    return jsonify(data)
