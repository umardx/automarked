from os import environ

broker_url = environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
result_backend = environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/1'
accept_content = ['application/json']
timezone = 'Asia/Jakarta'
enable_utc = True
