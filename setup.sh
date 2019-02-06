#!/bin/sh

cp ./.env.example ./.env

echo '[pip install pipenv]'
hash pipenv || pip install git+https://github.com/pypa/pipenv.git
echo '[pipenv install]'
pipenv install --dev

exit 0
