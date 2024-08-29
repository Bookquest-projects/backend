import cv2
import os
from flask import Blueprint, request, jsonify

from BookRepository import BookRepository
from ocr import OCR
from werkzeug.utils import secure_filename

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

    bookRepository = BookRepository()
    book_info = bookRepository.findBookByIsbn(isbn)
    if not book_info:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book_info), 200


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

    if not barcodes:
        return jsonify({"error": "No barcode found in image"}), 404

    isbns: list[str] = []
    for i in range(len(barcodes)):
        isbn = ocr.clean_isbn(barcodes[0].data.decode())
        if ocr.is_valid_code(isbn):
            isbns.append(isbn)

    if len(isbns) == 0:
        return jsonify({"error": "No valid ISBN in picture"}), 400

    return get_book_by_isbn(isbns[0])
