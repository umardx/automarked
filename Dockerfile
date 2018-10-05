FROM python:3.6-alpine

EXPOSE 8000
VOLUME [ "/src/database" ]

ENV APP_NAME 'Automarked'
ENV FLASK_ENV 'development'

ADD . /src/

RUN find /src/ -type d -exec chmod 755 {} \;
RUN find /src/ -type f -exec chmod 644 {} \;

WORKDIR /src/

RUN pip install pipenv
RUN pipenv install

ENTRYPOINT [ "pipenv", "run", "python" ]

CMD [ "run.py" ]