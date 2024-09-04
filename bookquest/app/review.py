from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from UserManager import UserManager
from ocr import OCR
from bookshelfManager import BookshelfManager
from reviewManager import ReviewManager

review_bp = Blueprint('reviews', __name__)

user_manager = UserManager()
review_manager = ReviewManager()
bookshelf_manager = BookshelfManager()


@review_bp.route('/reviews/<string:isbn>', methods=['GET'])
@jwt_required()
def get_review(isbn: str):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    ocr = OCR()
    if not ocr.is_valid_code(isbn):
        return jsonify({"error": "ISBN is not valid"}), 400

    current_username = get_jwt_identity()
    user_id = user_manager.get_userid(current_username)

    isbn_key = "isbn_13" if len(isbn) == 13 else "isbn_10"
    params = {
        isbn_key: isbn,
        "fk_user": user_id,
    }

    review = review_manager.get_review(params)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    review_infos = {
        'isbn_13': review.isbn_13 or "",
        'isbn_10': review.isbn_10 or "",
        'ratings': review.ratings or "",
        'favorite': review.favorite or False,
        'owned': review.owned or False,
        'reading_date': review.reading_date or "",
        'reading_number': review.reading_number or "",
        'comment': review.comment or ""
    }

    return jsonify(review_infos), 200


# TODO : Refactor to have a function with duplicated code!
@review_bp.route('/reviews/<string:isbn>/bookshelf', methods=['GET'])
@jwt_required()
def add_to_bookshelf(isbn: str):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    bookshelf_name = request.args.get('name', None)
    if not bookshelf_name:
        return jsonify({"error": "Bookshelf name is required"}), 400

    ocr = OCR()
    if not ocr.is_valid_code(isbn):
        return jsonify({"error": "ISBN is not valid"}), 400

    current_username = get_jwt_identity()
    user_id = user_manager.get_userid(current_username)
    bookshelf_id = bookshelf_manager.get_bookshelfid_by_name(
        bookshelf_name)

    isbn_key = "isbn_13" if len(isbn) == 13 else "isbn_10"
    params = {
        isbn_key: isbn,
        "fk_user": user_id,
    }

    review = review_manager.get_review(params)
    if not review:
        params['bookshelf'] = bookshelf_id
        success = review_manager.insert_review(params)
    else:
        updates = {'bookshelf': bookshelf_id}
        success = review_manager.update_review(review, updates)

    if not success:
        return jsonify({"error": "Error while saving the review"}), 404
    return jsonify(), 200


# TODO : Refactor to have a function with duplicated code!
@review_bp.route('/reviews/<string:isbn>/favorites', methods=['POST'])
@jwt_required()
def add_to_favorite(isbn: str):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    ocr = OCR()
    if not ocr.is_valid_code(isbn):
        return jsonify({"error": "ISBN is not valid"}), 400

    current_username = get_jwt_identity()
    user_id = user_manager.get_userid(current_username)

    isbn_key = "isbn_13" if len(isbn) == 13 else "isbn_10"
    params = {
        isbn_key: isbn,
        "fk_user": user_id,
    }

    review = review_manager.get_review(params)
    if not review:
        params['favorite'] = True
        success = review_manager.insert_review(params)
    else:
        updates = {'favorite': (False if review.favorite else True), }
        success = review_manager.update_review(review, updates)

    if not success:
        return jsonify({"error": "Error while saving the review"}), 404
    return jsonify(), 200


# TODO : Refactor to have a function with duplicated code!
@review_bp.route('/reviews/<string:isbn>/owned', methods=['POST'])
@jwt_required()
def add_to_owned(isbn: str):
    if not isbn:
        return jsonify({"error": "ISBN is required"}), 400

    ocr = OCR()
    if not ocr.is_valid_code(isbn):
        return jsonify({"error": "ISBN is not valid"}), 400

    current_username = get_jwt_identity()
    user_id = user_manager.get_userid(current_username)

    isbn_key = "isbn_13" if len(isbn) == 13 else "isbn_10"
    params = {
        isbn_key: isbn,
        "fk_user": user_id,
    }

    review = review_manager.get_review(params)
    if not review:
        params['owned'] = True
        success = review_manager.insert_review(params)
    else:
        updates = {'owned': (False if review.owned else True), }
        success = review_manager.update_review(review, updates)

    if not success:
        return jsonify({"error": "Error while saving the review"}), 404
    return jsonify(), 200
