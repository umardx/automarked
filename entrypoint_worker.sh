#!/bin/sh
pipenv run celery worker -A worker.celery --loglevel=info -E --concurrency=24
#pkill -9 -f 'celery worker'
