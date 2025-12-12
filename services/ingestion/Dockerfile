FROM python:3.12-slim

WORKDIR /app

COPY requirements_ingestion.txt .

RUN pip install --no-cache-dir -r requirements_ingestion.txt

COPY consumer.py .

CMD ["python", "consumer.py"]
