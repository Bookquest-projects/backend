import os

import cv2
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from BookRepository import BookRepository
from bookRecommender import BookRecommender
from helper import is_valid_isbn, clean_isbn
from ocr import OCR

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'image/png', 'image/jpg', 'image/jpeg'}  # TODO

books_bp = Blueprint('books', __name__)


@books_bp.route('/')
def hello_world():
    return "Hello, World! " + str(cv2.CV_64F + 1)


@books_bp.route('/books/<string:isbn>', methods=['GET'])
def get_book_by_isbn(isbn: str):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    isbn_cleaned = clean_isbn(isbn)
    bookRepository = BookRepository()
    if is_valid_isbn(isbn_cleaned):
        book_info = bookRepository.findBookByIsbn(isbn_cleaned)
        if not book_info:
            return jsonify({"error": "Book not found"}), 404

        return jsonify(book_info), 200
    else:
        return jsonify({"error": "Not a valid ISBN"}), 400


@books_bp.route('/books/scan', methods=['POST'])
def scan_book():
    if 'image' not in request.files:
        print("no image in data")
        return jsonify({"error": "image is required"}), 400

    file = request.files['image']
    if file.mimetype not in ALLOWED_EXTENSIONS:
        print("extension not allowed")
        return jsonify({"error": "Unsupported Media Type"}), 415

    fileName = secure_filename(file.filename)
    # create folder if missing
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    path = os.path.join(UPLOAD_FOLDER, fileName)
    file.save(path)

    ocr = OCR()
    barcodes = ocr.get_bar_code_info(ocr.imread(path))

    isbns: list[str] = []
    if not barcodes:
        txt = ocr.get_text_info(path)
        if len(txt) == 0:
            return jsonify({"error": "No isbn found in image"}), 404
        isbn = clean_isbn(txt)
        if is_valid_isbn(isbn):
            isbns.append(isbn)
    else:
        for i in range(len(barcodes)):
            isbn = clean_isbn(barcodes[0].data.decode())
            if is_valid_isbn(isbn):
                isbns.append(isbn)

    if len(isbns) == 0:
        return jsonify({"error": "No valid ISBN in picture"}), 400

    return get_book_by_isbn(isbns[0])


@books_bp.route('/books/<string:isbn>/recommendations', methods=['GET'])
def get_recommendations(isbn: str):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    if not is_valid_isbn(isbn):
        return jsonify({"error": "Not a valid ISBN"}), 400

    recommender = BookRecommender(isbn)
    recommendations = recommender.generate_recommendations()

    if not recommendations:
        return jsonify({"error": "Couldn't retrieve recommendations"}), 404

    return jsonify(recommendations), 200


@books_bp.route('/books/authors/<string:author>', methods=['GET'])
def get_author_books(author: str):
    if not author:
        return jsonify({"error": "author is required"}), 400

    lang = request.args.get('lang', None)

    bookRepository = BookRepository()
    books_info = bookRepository.find_books_by_author(author, lang)

    if not books_info:
        return jsonify({"error": "Couldn't retrieve books"}), 404

    return jsonify(books_info), 200


@books_bp.route('/books/series/<string:isbn>', methods=['GET'])
def get_series(isbn: str):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    return jsonify({"error": "Endpoint not implemented"}), 404
