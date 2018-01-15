FROM python:alpine

RUN mkdir -p /app/bildungsserver-content-crawler/
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD src/ /app/bildungsserver-content-crawler/
ADD data/ /app/data/

ENV PYTHONUNBUFFERED=1

ENTRYPOINT python -m bildungsserver-content-crawler.crawler
