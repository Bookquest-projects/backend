from flask import Flask, jsonify
import cv2

app = Flask(__name__)
myInt = cv2.CV_16F


@app.route('/')
def hello_world():
    return 'Hello World!' + ' ' + str(myInt) + ' ' + str(cv2.BORDER_CONSTANT)


@app.route('/data')
def data():
    return jsonify({"key": "value"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
