from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from BookRepository import BookRepository
from UserManager import UserManager
from bookshelfManager import BookshelfManager
from reviewManager import ReviewManager

bookshelf_bp = Blueprint('bookshelf', __name__)


user_manager = UserManager()
review_manager = ReviewManager()
bookshelf_manager = BookshelfManager()


@bookshelf_bp.route('/bookshelf', methods=['GET'])
def bookshelf_name():
    verify_jwt_in_request()
    current_username = get_jwt_identity()

    if 'name' not in request.args:
        return jsonify({"error": "Bookshelf name is required"}), 400

    ALLOWED_NAME = bookshelf_manager.get_all_bookshelf_name()
    print(ALLOWED_NAME)
    name = request.args.get('name')
    print(name)

    if name not in ALLOWED_NAME:
        print("Unsupported Bookshelf name: " + name)
        return jsonify({"error": "Unsupported Bookshelf name"}), 415


    user_id = user_manager.get_userid(current_username)
    bookshelf_id = bookshelf_manager.get_bookshelfid_by_name(name)

    isbns_13 = review_manager.get_isbns13_by_userid_and_bookshelfid(
        user_id, bookshelf_id)

    book_repository = BookRepository()
    books = []

    for isbn_13 in isbns_13:
        books.append(book_repository.findBookByIsbn(isbn_13))

    if len(books) == 0:
        return jsonify({"error": "No books for this bookshelf"}), 200

    return jsonify(books), 200
