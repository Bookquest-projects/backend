from userManager import UserManager
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, \
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    user_request = request.get_json()
    username = user_request.get('username')
    password = user_request.get('password')

    if user_manager.verify_user(username, password):
        access_token = create_access_token(identity=username)
        refresh_token = create_access_token(identity=username)
        response = jsonify()
        set_access_cookies(response, access_token, max_age=3600)  # 1 hour
        set_refresh_cookies(response, refresh_token,
                            max_age=86400)  # 24 hours
        return response, 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 403


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    user_request = request.get_json()
    username = user_request.get('username')
    password = user_request.get('password')

    try:
        user_manager.create_user(username, password)
        access_token = create_access_token(identity=username)
        refresh_token = create_access_token(identity=username)
        response = jsonify()
        set_access_cookies(response, access_token, max_age=3600)  # 1 hour
        set_refresh_cookies(response, refresh_token,
                            max_age=86400)  # 24 hours
        return response, 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 409


@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logged out"})
    unset_jwt_cookies(response)
    return response, 200
