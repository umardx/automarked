#!/bin/sh

echo '[flask db init...]'
pipenv run flask db init
echo '[flask db migrate...]'
pipenv run flask db migrate
echo '[flask db upgrade...]'
pipenv run flask db upgrade

pipenv run python run.py
