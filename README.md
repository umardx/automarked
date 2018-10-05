# Introduction Automarked
Atomarked is a web based application for configuration and management of network devices via Netconf using its Yang data model.
This web application is development using python flask and its still in the development.

## Important file and folder structure
```
$ tree automarked
automarked
|-- Pipfile
|-- README.md
|-- automarked
|   |-- __init__.py
|   |-- config.py
|   |-- models.py
|   |-- static
|   |   |-- css
|   |   |-- img
|   |   |-- js
|   |-- templates
|   |-- views.py
|   |-- yangModels
|-- run.py
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
3. Install environment

```sh
$ cd automarked
$ pipenv install --dev
```
4. Run app
```bash
$ pipenv run python run.py
```

## Docker
For fast and simple testing/development deployment, you can use the prepared docker image from my dockerhub repository.
```sh
$ mkdir ${PWD}/database
$ docker run -d --name automarked -v ${PWD}/database:/src/database -p 8000:8000/tcp umardx/automarked:latest
```