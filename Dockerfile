FROM python:3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV APP_FILE=app.py
EXPOSE 5000

COPY src/ .

ENTRYPOINT python $APP_FILE
