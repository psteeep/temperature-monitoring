from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from google.protobuf import json_format
from prometheus_pb2 import WriteRequest
import datetime


app = Flask(__name__)
HOST = '127.0.0.1'
PORT = 5003

# Конфігурація SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metrics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель для зберігання метрик
class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


# Ініціалізація бази даних
with app.app_context():
    db.create_all()


# Маршрут для отримання Remote Write запитів
@app.route('/write', methods=['POST'])
def write_metrics():
    try:
        # Прочитати байти даних з POST-запиту
        raw_data = request.data

        # Розпарсити дані у форматі Protocol Buffers
        write_request = WriteRequest()
        write_request.ParseFromString(raw_data)

        # Перетворити дані у JSON для зручної обробки
        write_request_json = json_format.MessageToDict(write_request)

        # Обробити кожну метрику в отриманому запиті
        for timeseries in write_request_json.get('timeseries', []):
            labels = {label['name']: label['value'] for label in timeseries.get('labels', [])}
            metric_name = labels.pop('__name__', 'unknown_metric')

            for sample in timeseries.get('samples', []):
                value = sample['value']
                timestamp_ms = sample['timestamp']
                timestamp = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)

                # Створити запис у базі даних
                new_metric = Metric(
                    value=value,
                    timestamp=timestamp
                )
                db.session.add(new_metric)

        # Зберегти всі записи
        db.session.commit()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Маршрут для перегляду збережених метрик
@app.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = Metric.query.all()
    return jsonify([
        {
            'value': metric.value,
            'timestamp': metric.timestamp.isoformat()
        } for metric in metrics
    ])


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
