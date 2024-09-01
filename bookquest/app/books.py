import os

import cv2
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from BookRepository import BookRepository
from ocr import OCR

UPLOAD_FOLDER = '../images'  # TODO
ALLOWED_EXTENSIONS = {'image/png', 'image/jpg', 'image/jpeg'}  # TODO

books_bp = Blueprint('books', __name__)


@books_bp.route('/')
def hello_world():
    return "Hello, World! " + str(cv2.CV_64F)


@books_bp.route('/books/<string:isbn>', methods=['GET'])
def get_book_by_isbn(isbn: str):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    ocr = OCR()
    isbn_cleaned = ocr.clean_isbn(isbn)
    bookRepository = BookRepository()
    if ocr.is_valid_code(isbn_cleaned):
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
    path = os.path.join(UPLOAD_FOLDER, fileName)
    file.save(path)

    ocr = OCR()
    barcodes = ocr.get_bar_code_info(ocr.imread(path))

    isbns: list[str] = []
    if not barcodes:
        txt = ocr.get_text_info(path)
        if len(txt) == 0:
            return jsonify({"error": "No isbn found in image"}), 404
        isbn = ocr.clean_isbn(txt)
        if ocr.is_valid_code(isbn):
            isbns.append(isbn)
    else:
        for i in range(len(barcodes)):
            isbn = ocr.clean_isbn(barcodes[0].data.decode())
            if ocr.is_valid_code(isbn):
                isbns.append(isbn)

        if len(isbns) == 0:
            return jsonify({"error": "No valid ISBN in picture"}), 400

    return get_book_by_isbn(isbns[0])
