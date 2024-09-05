from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from BookRepository import BookRepository
from UserManager import UserManager
from bookshelfManager import BookshelfManager
from reviewManager import ReviewManager

bookshelf_bp = Blueprint('bookshelf', __name__)

user_manager = UserManager()
review_manager = ReviewManager()
bookshelf_manager = BookshelfManager()
book_repository = BookRepository()


@bookshelf_bp.route('/bookshelf', methods=['GET'])
@jwt_required()
def bookshelf_name():
    try:
        current_username = get_jwt_identity()
        user_id = user_manager.get_userid(current_username)

        books = {}

        # Add all books for the bookshelfs
        bookshelf_names = bookshelf_manager.get_all_bookshelf_name()
        for bookshelf in bookshelf_names:
            bookshelf_id = bookshelf_manager.get_bookshelfid_by_name(
                bookshelf)
            params = {
                "fk_user": user_id,
                "fk_bookshelf": bookshelf_id
            }

            reviews = review_manager.get_all_reviews(params)
            shelf_books = []
            for review in reviews:
                shelf_books.append(
                    book_repository.findBookByIsbn(review.isbn_13))

            books[bookshelf] = shelf_books

        # Add the favorite and owned books
        names = ['favorite', 'owned']
        for name in names:
            params = {
                "fk_user": user_id,
                name: True
            }

            reviews = review_manager.get_all_reviews(params)
            shelf_books = []
            for review in reviews:
                shelf_books.append(
                    book_repository.findBookByIsbn(review.isbn_13))

            books[name] = shelf_books

        return jsonify(books), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
