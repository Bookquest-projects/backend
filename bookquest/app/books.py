import cv2
from flask import Blueprint, request, jsonify

from bookquest.app.BookRepository import BookRepository

books_bp = Blueprint('books', __name__)


@books_bp.route('/')
def hello_world():
    return "Hello, World! " + str(cv2.CV_64F)


@books_bp.route('/books/<string:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    bookRepository = BookRepository()
    book_info = bookRepository.findBookByIsbn(isbn)
    if not book_info:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"book_info": book_info})


@books_bp.route('/books/scan', methods=['POST'])
def scan_book():
    image = request.files['image']

    # save the image in /app
    image.save('image.jpg')

    if not image:
        return jsonify({"error": "Image is required"}), 400

    # TODO OCR

    # TODO return book
    return jsonify({}, 200)
