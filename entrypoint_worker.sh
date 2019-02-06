#!/bin/sh
virtenv="$(pipenv --venv)/bin/activate"
. $virtenv

sysctl vm.overcommit_memory=1
echo never > /sys/kernel/mm/transparent_hugepage/enabled
celery worker -A worker.celery --loglevel=info -E --concurrency=24
#pkill -9 -f 'celery worker'
