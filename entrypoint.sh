#!/bin/bash

virtenv="$(pipenv --venv)/bin/activate"
. $virtenv

mkdir -p log

run_webapp () {
    if [ ! -d 'migrations' ]; then
    echo '[flask db init...]'
    flask db init
    fi
    echo '[flask db migrate...]'
    flask db migrate
    echo '[flask db upgrade...]'
    flask db upgrade
    echo '[pipenv run python run.py]'
    python run.py
}

run_worker () {
    pokemons="Pikachu Raichu Bulbasaur Ivysaur Venusaur Charmander Charmeleon Charizard"
    for pokemon in ${pokemons}; do
        watchmedo auto-restart --recursive --pattern="task.py" --directory="." -- \
        celery worker -A run.celery --loglevel=info --concurrency=8 \
        -n ${pokemon}@%h >> log/worker_${pokemon}.log 2>&1 &
    done
    celery -A run.celery flower \
    --logging=debug >> log/flower.log 2>&1 &
    tail -f log/worker*.log log/flower.log
}


if [ $# -gt 0 ]; then
    if [ "$*" = "worker" ]; then
        run_worker
    else
        exec $@
    fi
else
    run_webapp
fi

