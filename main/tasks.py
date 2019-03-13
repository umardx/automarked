from main import celery
from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.errors import YModelError, YCodecError, YCoreError, YError, YClientError
from main.models import NetConf, Devices
from requests import post
import json

json_provider = CodecServiceProvider(type='json')
codec = CodecService()


@celery.task(time_limit=10)
def netconf(message):
    data = message.get('data')
    json_data = [json.dumps({k:v}) for k, v in data.items()]

    sid = message.get('sid')
    url = message.get('url')

    errors = []
    response = {}
    try:
        _codec = codec.decode(json_provider,  json_data)
    except (RuntimeError, ValueError, IndexError, YModelError, YCodecError, YCoreError) as err:
        _codec = None
        errors.append(str(err))

    if _codec is not None:
        device_id = message.get('device_id')
        device = Devices.query.filter_by(id=device_id).first()
        operation = message.get('operation')

        try:
            nc = NetConf(device.host, device.port, device.username, device.password)
        except (RuntimeError, YClientError) as err:
            nc = None
            errors.append(str(err))

        if nc is not None:
            if operation == 'get-config':
                try:
                    _gets = nc.get_config(read_filter=_codec)
                except (RuntimeError, YError) as err:
                    _gets = None
                    errors.append(str(err))

                if _gets is not None:
                    for _get in _gets:
                        _response = codec.encode(json_provider, _get)
                        response.update(json.loads(_response))

            elif operation == 'edit-config':
                try:
                    _gets = nc.edit_config(config=_codec) and nc.commit()
                except (RuntimeError, YError) as err:
                    _gets = None
                    errors.append(str(err))

                if _gets:
                    response = {
                        'operation': 'success'
                    }

    if len(errors) == 0:
        errors = None

    payload_dict = {
        'room': sid,
        'message': {
            'error': errors,
            'data': response
        }
    }

    payload = json.dumps(payload_dict)
    res = {'request': post(url, payload), 'codec': _codec, payload: payload}
    return str(res)

