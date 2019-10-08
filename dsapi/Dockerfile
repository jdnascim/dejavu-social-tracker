FROM python:3.7-alpine AS base

RUN mkdir home/app
WORKDIR home/app

COPY Pipfile .
COPY Pipfile.lock .
COPY core/ ./core
COPY api/ .

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

# Necessary libraries to build psycopg2
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk update && apk upgrade
RUN apk add --no-cache bash git openssh
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk add libxml2
RUN apk add libjpeg
RUN apk --update add libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install

EXPOSE 5000
# Points to the current dir as our app factory for flask
ENV FLASK_APP /home/app/src/app.py
# Add current dir to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/home/app"
ENTRYPOINT pipenv run flask run --host=0.0.0.0 --port=5000
