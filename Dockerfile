FROM python:2.7

MAINTAINER Angelo Suinan <suinanangelo@gmail.com>

RUN mkdir /web
WORKDIR /web

ADD ./src/requirements.txt /web/requirements.txt
RUN pip install -r requirements.txt
