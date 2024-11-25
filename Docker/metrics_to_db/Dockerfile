FROM python:3.10-alpine

WORKDIR /app

COPY ./services/metrics_to_db.py .
COPY ./Docker/metrics_to_db/requirements.txt .
COPY ./services/prometheus_pb2.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5003

CMD ["python", "metrics_to_db.py"]
