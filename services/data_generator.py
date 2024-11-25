from flask import Flask, Response
import random


app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000


def _get_current_cpu_temperature():
    try:
        # Generate current cpu temperature
        temperature = random.triangular(20.0, 60.0) + random.uniform(0.0, 20.0)
        # OPTIONAL: add cross-platform solution to get real current cpu temperature
    except Exception as exception:
        print(f'Can not get current cpu temperature: {exception}')
        temperature = "N/A"  # If we can`t get current cpu temperature
    return temperature


@app.route('/metrics')
def metrics():
    temperature = _get_current_cpu_temperature()
    # Metrics in Prometheus format
    response = f"""
                    # HELP server_temperature Current temperature of the server in Celsius.
                    # TYPE server_temperature gauge
                    server_temperature {temperature}

                    """

    return Response(response, mimetype="text/plain")


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)