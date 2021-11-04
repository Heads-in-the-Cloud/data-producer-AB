FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY users-producer.py .
CMD ["python","users-producer.py"]
