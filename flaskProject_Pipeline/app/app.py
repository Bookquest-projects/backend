from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/data')
def data():
    return jsonify({"key": "value"})


if __name__ == '__main__':
    app.run()
