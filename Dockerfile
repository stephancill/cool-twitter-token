FROM python:3.7

LABEL MAINTAINER="Stephan Cilliers <stephanus.cilliers@protonmail.com>"

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apt update 
RUN pip install 'pipenv==2018.11.26'
RUN pipenv install --system --ignore-pipfile

RUN chmod +x wait-for-it.sh
RUN chmod +x docker-entrypoint.sh

CMD ["alembic", "upgrade", "head"]
