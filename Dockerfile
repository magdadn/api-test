FROM python:3.6.4-slim-jessie

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 7000


