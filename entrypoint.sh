#!/bin/sh

echo '[flask db init...]'
if [ ! -d "database" ]; then
pipenv run flask db init
fi
echo '[flask db migrate...]'
pipenv run flask db migrate
echo '[flask db upgrade...]'
pipenv run flask db upgrade

pipenv run python run.py
