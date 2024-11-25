from flask import Flask, Response
from prometheus_client import Gauge, generate_latest
import random

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000

temperature_gauge = Gauge('server_temperature', 'Current temperature of the server in Celsius')


def _get_current_cpu_temperature():
    try:
        temperature = random.triangular(20.0, 60.0) + random.uniform(0.0, 20.0)
        temperature_gauge.set(temperature)
    except Exception as exception:
        print(f'Can not get current cpu temperature: {exception}')
        temperature = "N/A"
    return temperature


@app.route('/metrics')
def metrics():
    _get_current_cpu_temperature()
    response = generate_latest()
    return Response(response, mimetype="text/plain")


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
