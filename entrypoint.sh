#!/bin/bash

virtenv="$(pipenv --venv)/bin/activate"
. $virtenv

rm -rf log
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
    echo '[run the server]'
    python run.py 2>&1 |& tee -a log/webapp.log &
    tail -f log/webapp.log
}

run_worker () {
#    pokemons="Pikachu Raichu Bulbasaur Ivysaur Venusaur Charmander Charmeleon Charizard"
    pokemons="Pikachu"
    for pokemon in ${pokemons}; do
        celery worker -A run.celery -l info -n ${pokemon}@%h \
        2>&1 |& tee -a log/worker.log &
    done
    celery -A run.celery flower -l debug \
    2>&1 |& tee -a log/flower.log &
    tail -f log/worker.log log/flower.log
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

