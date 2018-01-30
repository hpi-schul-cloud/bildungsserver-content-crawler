FROM python:alpine

RUN mkdir -p /app/
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD src/ /app/src/
ADD src/schema/ /app/src/schema/
ADD app.py /app/
ADD data/ /app/data/

ENV PYTHONUNBUFFERED=1

ENTRYPOINT python -m app
