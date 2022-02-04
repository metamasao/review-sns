FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERD 1

WORKDIR /social-website

COPY Pipfile Pipfile.lock /social-website/
RUN pip install pipenv && pipenv install --system

COPY . /social-website/