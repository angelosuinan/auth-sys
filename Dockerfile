FROM python:2.7

MAINTAINER Angelo Suinan <suinanangelo@gmail.com>

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev libffi-dev

RUN apt-get -y autoremove

RUN mkdir /web
WORKDIR /web
ADD ./src/requirements.txt /web/requirements.txt
RUN pip install -r requirements.txt
