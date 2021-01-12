FROM python:3.8

RUN apt-get update

WORKDIR /app

ADD . /app

ENV PORT 8080

RUN pip install -r requirements.txt

CMD python3 app.py