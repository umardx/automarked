# Introduction Automarked
Atomarked is a web based application for configuration and management of network devices via Netconf using its Yang data model.
This web application is development using python flask and its still in the development.

## Important file and folder structure after setup
```
.
├── main
│   ├── auth
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── views.py
│   ├── config.py
│   ├── dashboard
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── views.py
│   ├── home
│   │   ├── __init__.py
│   │   └── views.py
│   ├── __init__.py
│   ├── models.py
│   ├── static
│   │   ├── css
│   │   ├── img
│   │   ├── js
│   │   └── plugins
│   └── templates
│       ├── auth
│       ├── _auth.html
│       ├── dashboard
│       ├── _dashboard.html
│       ├── home
│       └── _home.html
├── database
│   └── app.db
├── Dockerfile
├── entrypoint.sh
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── 5ff916efd69b_.py
├── Pipfile
├── Pipfile.lock
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
3. Install python environment via `pipenv`

```sh
$ cd automarked
$ pipenv install --dev
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
(automarked-pZFT...)$ pipenv run python run.py
```

## Docker
For fast and simple testing/development deployment, you can use the prepared docker image from my dockerhub repository.
```sh
$ mkdir ${PWD}/database
$ docker run -d --name automarked \
-v ${PWD}/database:/main/database \
-p 8000:8000/tcp umardx/automarked:latest
```
