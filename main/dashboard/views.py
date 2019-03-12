from flask import flash, redirect, url_for, \
    render_template, request, jsonify, session
from flask_login import login_required, current_user
from flask_socketio import emit as s_emit
from sqlalchemy import asc

import json

from main.dashboard import dashboard
from main.dashboard.forms import add_device_form, edit_device_form
from main import db
from main.models import Devices, NetConf, YangModel


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

    action = request.args.get('action')
    device_id = request.args.get('device_id')

    if action == 'refresh':
        refresh(device_id)
        return redirect(url_for('dashboard.list_device'))
    elif action == 'refresh_all':
        refresh_all()
        return redirect(url_for('dashboard.list_device'))
    elif action == 'delete':
        delete(device_id)
        return redirect(url_for('dashboard.list_device'))
    elif action == 'telemetry':
        return redirect(url_for('dashboard.list_device'))
    elif action == 'netconf':
        session['device_id'] = device_id
        return redirect(url_for('dashboard.netconf'))

    return render_template(
        'dashboard/list_device.html',
        title='List Device | Dashboard',
        form_edit_device=form_edit_device,
        devices=Devices.query.filter_by(
            user_id=current_user.id
        ).all(),
        device_id=device_id
    )


@login_required
def refresh(id):
    _device = Devices.query.filter_by(id=id).first()
    _device.update_status()

    try:
        db.session.commit()
        flash(
            u'The device was successfully refreshed.',
            'success'
        )
    except Exception as e:
        flash(u'Can\'t refresh the device. ' + str(e), 'error')


@login_required
def refresh_all():
    devices = Devices.query.filter_by(
        user_id=current_user.id
    ).all()
    for _device in devices:
        _device.update_status()

    try:
        db.session.commit()
        return flash(
            u'All devices are successfully refreshed.',
            'success'
        )
    except Exception as err:
        return flash(u'Can\'t refresh all device. ' + str(err), 'error')


@login_required
def delete(id):
    _device = Devices.query.filter_by(id=id).first()

    try:
        db.session.delete(_device)
        db.session.commit()
        flash(u'You were successfully deleted the device.', 'success')
    except Exception as err:
        flash(u'Can\'t delete device. ' + str(err), 'error')


@login_required
def edit(device, id):
    _device = Devices.query.filter_by(id=id).first()
    try:
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


# Endpoint for edit device
@dashboard.route('/device/<device_id>')
@login_required
def device(device_id):
    data = dict()
    _device = Devices.query.filter_by(id=device_id).first()
    if _device is not None:
        data['id'] = _device.id
        data['host'] = _device.host
        data['port'] = _device.port
        data['username'] = _device.username
        data['password'] = _device.password

    return jsonify(data)


# route netconf
@dashboard.route('/netconf')
@login_required
def netconf():
    """
    Handle requests to the /dashboard/netconf route
    Show netconf dashboard display
    """

    _device_id = None

    if 'device_id' in session:
        _device_id = session['device_id']
        _device = Devices.query.filter_by(id=_device_id).first()

        session.pop('device_id', None)

    return render_template(
        'dashboard/netconf.html',
        title='Network Configuration',
        devices=Devices.query.filter_by(
            user_id=current_user.id
        ).order_by(asc(Devices.host)).all(),
        device_id=_device_id,
        operations=NetConf.support_operations(),
        models=YangModel.support_models()
    )


@dashboard.route('/netconf/emit', methods=['POST'])
def emit():
    try:
        data = json.loads(request.get_data().decode("utf-8"))
        room = data.get('room')
        message = data.get('message')
        s_emit('render_res', message, room=room, namespace='/nc')
    except:
        message = {}

    return jsonify(message)
