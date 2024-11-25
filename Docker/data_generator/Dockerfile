FROM python:3.10-alpine

WORKDIR /app

COPY ./services/data_generator.py .

RUN pip install flask

EXPOSE 5000

CMD ["python", "data_generator.py"]
