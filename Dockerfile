FROM python:3.10.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app



