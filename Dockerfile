# syntax=docker/dockerfile:1


FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /code
RUN chown -Rh $user:$user /code
USER $user

COPY . /code/
COPY requirements.txt /code/

RUN apt update && apt -y install curl \ 
    && apt -y install python3 \
    && apt-get -y install python3-pip \
    && apt-get -y install libpq-dev \
    && apt-get -y install python3-tk

RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1