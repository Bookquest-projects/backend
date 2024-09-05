from flask import Blueprint, request, jsonify
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

        if 'name' not in request.args:
            return jsonify({"error": "Bookshelf name is required"}), 400

        name = request.args.get('name')
        if name in ['favorite', 'owned']:
            user_id = user_manager.get_userid(current_username)
            params = {
                "fk_user": user_id,
                name: True
            }
        else:
            allowed_name = bookshelf_manager.is_bookshelf_name_allowed(name)
            if not allowed_name:
                return jsonify({"error": "Unsupported Bookshelf name"}), 415

            user_id = user_manager.get_userid(current_username)
            bookshelf_id = bookshelf_manager.get_bookshelfid_by_name(name)
            params = {
                "fk_user": user_id,
                "fk_bookshelf": bookshelf_id
            }

        reviews = review_manager.get_review(params)

        books = []
        for review in reviews:
            books.append(book_repository.findBookByIsbn(review.isbn_13))

        return jsonify(books), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
