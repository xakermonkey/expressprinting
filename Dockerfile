FROM python:3.8.10


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/apps


COPY requirements.txt /opt/apps/

RUN pip install -r requirements.txt

COPY . /opt/apps