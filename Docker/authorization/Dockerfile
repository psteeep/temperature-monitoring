FROM python:3.10-alpine

WORKDIR /app

COPY ./services/authorization.py .
COPY ./Docker/authorization/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "authoriazation.py"]
