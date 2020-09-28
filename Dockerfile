FROM python:3.7-alpine
MAINTAINER John Smith

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
       gcc libc-dev linux-headers python3-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./twitterapi /app

RUN adduser -D user
USER user