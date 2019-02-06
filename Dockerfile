FROM ubuntu:18.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Install Pipenv:
RUN apt-get update -qq && \
apt-get install python3.6 python3-pip \
gdebi-core gcc-5 g++-5 libtool-bin wget -yqq

# Backwards compatility.
RUN rm -fr /usr/bin/python3 && ln /usr/bin/python3.6 /usr/bin/python3
RUN ln -fs /usr/bin/g++-5 /usr/bin/c++
RUN ln -fs /usr/bin/gcc-5 /usr/bin/cc

RUN pip3 install pipenv

WORKDIR /opt

RUN wget https://devhub.cisco.com/artifactory/debian-ydk/0.8.0/bionic/libydk_0.8.0-1_amd64.deb
RUN gdebi -n libydk_0.8.0-1_amd64.deb

WORKDIR /app

COPY . /app

RUN pipenv install --dev

ENTRYPOINT [ "/bin/sh" ]

CMD [ "entrypoint.sh" ]
