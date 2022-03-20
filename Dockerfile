FROM python:3.8-slim-buster

WORKDIR ./planta-api

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . ./entrevista-planta-energia-master