# Introduction Automarked
Atomarked is a web based application for configuration and management of network devices via Netconf using its Yang data model.
This web application is development using python flask and its still in the development.

## Important file and folder structure
```sh
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
```bash
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