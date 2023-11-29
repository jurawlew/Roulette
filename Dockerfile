FROM python:3.10

RUN mkdir /roulette
WORKDIR /roulette
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt update
