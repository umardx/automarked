from app import celery
from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.errors import YModelError, YCodecError, YCoreError
from requests import post
import json
import time


@celery.task(time_limit=5)
def netconf(data, sid, url):
    time.sleep(1)
    json_provider = CodecServiceProvider(type='json')
    codec = CodecService()

    try:
        _codec = codec.decode(json_provider,  json.dumps(data))
        payload = json.dumps({
            'room': sid,
            'message': {
                'error': None,
                'data': {
                    'Dummy-response': {}
                },
            }
        })
    except (RuntimeError, ValueError, IndexError, YModelError, YCodecError, YCoreError) as err:
        _codec = None
        payload = json.dumps({
            'room': sid,
            'message': {
                'error': str(err),
                'data': {},
            }
        })

    res = {'request': post(url, payload), 'codec': _codec}
    return str(res)

