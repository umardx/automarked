#!/bin/bash
pipenv run celery worker -A worker.celery --loglevel=info -E
#pkill -9 -f 'celery worker'
