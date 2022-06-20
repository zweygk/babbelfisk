# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN python -m spacy download en_core_web_sm

ENV FLASK_APP app.py
EXPOSE 5002

COPY . .

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5002"]