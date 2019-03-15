# Introduction Automarked
Atomarked is a web based application for configuration and management of network devices via Netconf using its Yang data model.
This web application is development using python flask and its still in the development.

## Important file and folder structure after setup
```sh
$ tree -L 2 .
./
├── database
│   └── app.db
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── log
├── main
│   ├── auth
│   ├── config_app.py
│   ├── config_celery.py
│   ├── dashboard
│   ├── events.py
│   ├── home
│   ├── __init__.py
│   ├── models.py
│   ├── __pycache__
│   ├── static
│   ├── tasks.py
│   └── templates
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── __pycache__
│   ├── README
│   ├── script.py.mako
│   └── versions
├── Pipfile
├── __pycache__
│   └── run.cpython-36.pyc
├── README.md
├── run.py
└── setup.sh

```

## Setup
1. Clone this repo
```sh
$ git clone https://github.com/umardx/automarked.git
```
2. Install pipenv via pip. To install pip, use the following [link](https://pip.pypa.io/en/stable/installing/) or by an easy way you think, as long as there is a `pip` on your OS.
```sh
$ pip install pipenv
```
3. Install python packages via `pipenv`

```sh
$ cd automarked
$ pipenv install --dev
```
or
```sh
$ cd automarked
$ pipenv run pip install -r .requirements.txt
```
4. Enter mode virtualenv via `pipenv`
```sh
$ pipenv shell
```
5. Intialize db
```sh
(automarked-pZFT...)$ flask db init
(automarked-pZFT...)$ flask db migrate
(automarked-pZFT...)$ flask db upgrade 
```
6. Run app
```sh
(automarked-pZFT...)$ python run.py
```

`Important` : to activate websocket emit from task queue, add the following line to file hosts at `/etc/hosts`:
```bash
127.0.0.1	localhost webapp redis
``` 

## Docker
For fast and simple testing/development deployment, you can use the prepared docker image from my dockerhub repository.
There are three services namely webapp as web service, worker as task queue service, and redis as message broker service.
You can do deploy with `docker-compose` in this repo root directory as follows:
```sh
$ cd automarked
$ docker-compose up -d --build
or
$ docker-compose up -d
```
And then open url : `http://localhost:8000` at the browser.
To monitor task queue and the broker running, open url `http://localhost:8888`
