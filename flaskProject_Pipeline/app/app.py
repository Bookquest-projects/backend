from flask import Flask, jsonify, request
from BookRepository import BookRepository
import cv2

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello, World! " + str(cv2.CV_64F)


@app.route('/book', methods=['GET'])
def get_book_by_isbn():
    isbn = request.args.get('isbn')
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    bookRepository = BookRepository()
    book_info = bookRepository.findBookByIsbn(isbn)
    if not book_info:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"book_info": book_info})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
