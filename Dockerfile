FROM python:3.9-slim

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/* \

RUN pip install --upgrade pip
RUN pip install wheel

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
