import cv2
from flask import Blueprint, request, jsonify

from BookRepository import BookRepository

books_bp = Blueprint('books', __name__)


@books_bp.route('/')
def hello_world():
    return "Hello, World! " + str(cv2.CV_64F)


@books_bp.route('/book', methods=['GET'])
def get_book_by_isbn():
    isbn = request.args.get('isbn')

    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    bookRepository = BookRepository()
    book_info = bookRepository.findBookByIsbn(isbn)
    if not book_info:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"book_info": book_info})
