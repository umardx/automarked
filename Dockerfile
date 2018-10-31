FROM ubuntu:18.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Install Pipenv:
RUN apt update -qq && apt install python3.6 python3-pip -yqq

# Backwards compatility.
RUN rm -fr /usr/bin/python3 && ln /usr/bin/python3.6 /usr/bin/python3

RUN pip3 install pipenv

WORKDIR /app

COPY . /app

RUN pipenv install --dev

ENTRYPOINT [ "/bin/sh" ]

CMD [ "entrypoint.sh" ]
