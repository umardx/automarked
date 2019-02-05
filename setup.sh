#!/bin/sh

cp ./.env.example ./.env

echo '[pip install pipenv]'
pip install pipenv
echo '[pipenv install]'
pipenv install --dev

start_redis.sh &

exit 0
