from os import environ

broker_url = environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
result_backend = environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/1'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

task_eager_propagates = True
task_ignore_result = True

timezone = 'Asia/Jakarta'
enable_utc = True
