FROM python:3-alpine

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

ENTRYPOINT python install -r requirements.txt
