#!/bin/sh
pipenv run flower --broker=redis://127.0.0.1:6379/0 --port=8080
