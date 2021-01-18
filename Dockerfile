FROM python:3.8

RUN apt-get update

COPY . /usr/app/

WORKDIR /usr/app/

EXPOSE 5000

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

ENV PORT 8080

CMD python app.py

