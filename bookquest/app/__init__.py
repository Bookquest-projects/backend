import os

from flask import Flask
from flask.cli import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(
        app,
        origins=os.getenv("ORIGIN"),
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        supports_credentials=True
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # BLUEPRINTS #
    from auth import auth_bp
    from books import books_bp
    from bookshelf import bookshelf_bp

    app.register_blueprint(bookshelf_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(auth_bp)

    # JWT CONFIGURATION #
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']

    JWTManager(app)

    return app


# DATABASE CONFIGURATION #
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("SQLSERVER_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")

# reflect the tables
Base = automap_base()
engine = create_engine(
    f"mssql+pytds://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)
Base.prepare(engine)

# mapped classes
User = Base.classes.user
Review = Base.classes.review
Bookshelf = Base.classes.bookshelf

session = Session(engine)

if __name__ == '__main__':
    app = create_app()
    DEBUG = os.getenv("DEBUG")
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
