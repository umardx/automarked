FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN apt-get update -qq && \
    apt-get install python3.6 python3-pip apt-utils \
    gdebi-core gcc-5 g++-5 libtool-bin wget -yqq

WORKDIR /app

RUN rm -rf /usr/bin/python3 && \
    ln /usr/bin/python3.6 /usr/bin/python3 && \
    ln -fs /usr/bin/g++-5 /usr/bin/c++ && \
    ln -fs /usr/bin/gcc-5 /usr/bin/cc && \
    pip3 install pipenv && \
    wget -q https://devhub.cisco.com/artifactory/debian-ydk/0.8.0/bionic/libydk_0.8.0-1_amd64.deb && \
    gdebi -n libydk_0.8.0-1_amd64.deb && \
    rm -rf {,.[!.],..?}*

COPY . /app

RUN pipenv install

ENTRYPOINT [ "/bin/sh", "entrypoint_app.sh" ]