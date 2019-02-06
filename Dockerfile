FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . /app

RUN apt-get update -qq \
    && apt-get -yqq install python3.6 \
    python3-dev libtool-bin apt-utils \
    gcc-5 g++-5 libtool-bin git curl gdebi-core \
    && ln -fs /usr/bin/g++-5 /usr/bin/c++ \
    && ln -fs /usr/bin/gcc-5 /usr/bin/cc \
    && curl -s https://devhub.cisco.com/artifactory/debian-ydk/0.8.0/bionic/libydk_0.8.0-1_amd64.deb \
    -o libydk_0.8.0-1_amd64.deb \
    && gdebi -n libydk_0.8.0-1_amd64.deb \
    && rm libydk_0.8.0-1_amd64.deb \
    && chmod +x ./entrypoint*.sh \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.6 10 \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    && pip install git+https://github.com/pypa/pipenv.git

RUN pipenv install
ENTRYPOINT [ "sh", "entrypoint_app.sh" ]
