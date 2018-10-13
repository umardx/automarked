FROM python:3.6-alpine

WORKDIR /app

COPY . /app

RUN sh ./setup.sh

ENTRYPOINT [ "/bin/sh" ]

CMD [ "entrypoint.sh" ]
