#!/bin/bash
pipenv run celery worker -A worker.celery --loglevel=info -E
