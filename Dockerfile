FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . .

RUN apt-get update -qq \
    && apt-get -yqq install python3.6 \
    python3-dev libtool-bin git curl  \
    gcc-5 g++-5 libtool-bin gdebi-core nano \
    && ln -fs /usr/bin/g++-5 /usr/bin/c++ \
    && ln -fs /usr/bin/gcc-5 /usr/bin/cc \
    && curl -sL https://devhub.cisco.com/artifactory/debian-ydk/0.8.1/bionic/libydk_0.8.1-2_amd64.deb \
    -o libydk_amd64.deb \
    && gdebi -n libydk_amd64.deb \
    && rm libydk_amd64.deb \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.6 10 \
    && useradd -ms /bin/bash automarked \
    && chown -R automarked:automarked . \
    && curl -sL https://bootstrap.pypa.io/get-pip.py | python \
    && pip install pipenv \
    && rm -rf /var/lib/apt/lists/*

USER automarked

WORKDIR /app

RUN cp .env.example .env \
    && chmod +x ./entrypoint*.sh \
    && pipenv run pip install -r .requirements.txt

ENTRYPOINT [ "./entrypoint.sh" ]
