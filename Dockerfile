FROM python:3.8

RUN apt-get update

WORKDIR /app

ADD . /app

ENV PORT 8080

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

CMD python3 app.py

