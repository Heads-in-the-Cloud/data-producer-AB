FROM python:3

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/ .

EXPOSE 5000
ENTRYPOINT python app
