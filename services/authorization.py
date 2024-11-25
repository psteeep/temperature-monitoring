from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests


JWT_SECRET_KEY = 'jwt_secret_key'
HOST = '127.0.0.1'
PORT = 5001
GRAFANA_URL = "http://127.0.0.1:5002"  # "http://grafana:3000"


# Flask initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Create database for users' usernames and passwords
with app.app_context():
    db.create_all()


# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# User authorization
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200


# TEST: Protected route
# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify({'message': f'Hello, {current_user}! This is a protected route.'}), 200


# Реверсивний проксі для Grafana TODO: перевірити роботу з реальною Grafana
@app.route('/grafana/<path:path>', methods=['GET'])  #  , 'POST', 'PUT', 'DELETE'
@jwt_required()  # Авторизація через JWT
def proxy_to_grafana(path):
    current_user = get_jwt_identity()  # Отримуємо інформацію про користувача
    headers = {key: value for key, value in request.headers if key != 'Host'}
    headers['X-User'] = current_user  # Додаємо інформацію про користувача

    # Пересилаємо запит до Grafana
    grafana_response = requests.request(
        method=request.method,
        url=f"{GRAFANA_URL}/{path}",
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    # Формуємо відповідь для клієнта
    response = jsonify(grafana_response.json() if grafana_response.content else {})
    response.status_code = grafana_response.status_code
    return response


# Run authorization app
if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)

# # Example of usage:
# import requests
# # Register new user
# requests.post('http://127.0.0.1:5001/register', json={"username": "testuser", "password": "securepassword"})
# # Log in and get access token
# access_token = requests.post('http://127.0.0.1:5001/login',
#                              json={"username": "testuser", "password": "securepassword"}).json()['access_token']
# # Use access token to connect to the protected route
# requests.get('http://127.0.0.1:5001/protected', headers={"Authorization": f"Bearer {access_token}"})#.json()
# # OR use access token to connect to the grafana_test
# requests.get('http://127.0.0.1:5002/api/dashboards', headers={"Authorization": f"Bearer {access_token}"}).json()
