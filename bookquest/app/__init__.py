from flask import Flask
from flask_cors import CORS

from bookquest.app.auth import auth_bp
from books import books_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(books_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
