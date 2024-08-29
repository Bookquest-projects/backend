import os

from flask import Flask
from flask.cli import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from bookquest.app.auth_api import auth_bp
from bookquest.app.books import books_bp

app = Flask(__name__)
CORS(
    app,
    origins='http://localhost:5173',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    supports_credentials=True
)
app.register_blueprint(books_bp)
app.register_blueprint(auth_bp)

# Configuration
load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
