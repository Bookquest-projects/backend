import os

import sqlalchemy
from flask import Flask
from flask.cli import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app():
    from auth import auth_bp
    from books import books_bp
    app = Flask(__name__)
    CORS(
        app,
        origins='http://localhost:5173',
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        supports_credentials=True
    )

    load_dotenv()
    # JWT Configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']

    # DB Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(books_bp)
    app.register_blueprint(auth_bp)
    jwt = JWTManager(app)

    return app


if __name__ == '__main__':
    app = create_app()
    engine = sqlalchemy.create_engine(
        os.getenv("DATABASE_URI")
    )

    app.run(host="0.0.0.0", port=5000)
