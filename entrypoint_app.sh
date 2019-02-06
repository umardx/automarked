#!/bin/sh -x
virtenv="$(pipenv --venv)/bin/activate"
. $virtenv

echo '[flask db init...]'
flask db init
echo '[flask db migrate...]'
flask db migrate
echo '[flask db upgrade...]'
flask db upgrade
echo '[pipenv run python run.py]'
python run.py
