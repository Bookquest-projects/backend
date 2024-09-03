from .db import DatabaseManager
from .UserManager import UserManager
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, \
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)

database = DatabaseManager('host',
                           'user',
                           'password',
                           'database')  # TODO : How to acces to DB
user_manager = UserManager(database)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    user_request = request.get_json()
    username = user_request.get('username')
    password = user_request.get('password')

    is_valid = user_manager.verify_user(username, password)

    if not is_valid:
        return jsonify({"msg": "Invalid user"}), 403
    else:
        access_token = create_access_token(identity=username)
        refresh_token = create_access_token(identity=username)
        response = jsonify()
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 201


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    user_request = request.get_json()
    username = user_request.get('username')
    password = user_request.get('password')

    is_valid = user_manager.create_user(username, password)

    if not is_valid:
        return jsonify({"msg": "User already exists"}), 409
    else:
        access_token = create_access_token(identity=username)
        refresh_token = create_access_token(identity=username)
        response = jsonify()
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 201


@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout"})
    unset_jwt_cookies(response)
    return response, 200
