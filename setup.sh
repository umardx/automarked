#!/bin/sh

echo '[PWD]'
pwd

cp ./.env.example ./.env

echo '[pip install pipenv]'
pip install pipenv
echo '[pipenv install]'
pipenv install

exit 0
