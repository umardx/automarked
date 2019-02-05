#!/bin/bash
pipenv run celery worker -A worker.celery --loglevel=info -E --concurrency=24
#pkill -9 -f 'celery worker'
#flower --broker=redis://127.0.0.1:6379/0 --port=8080
