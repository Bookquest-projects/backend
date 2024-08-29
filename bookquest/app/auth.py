from db import DatabaseManager
from UserManager import UserManager
from flask import request, jsonify, Blueprint

auth_bp = Blueprint('auth', __name__)
database = DatabaseManager('host', 'user', 'password', 'database')
user_manager = UserManager(database)


@auth_bp.route('/user', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing 'username' or 'password'"}), 400

    try:
        user_manager.create_user(data['username'], data['password'])
        return jsonify({"message": "User created successfully."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify(
            {"error": "An error occurred during user creation."}), 500


@auth_bp.route('/user/verify', methods=['POST'])
def verify_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing 'username' or 'password'"}), 400

    is_valid = user_manager.verify_user(data['username'], data['password'])
    if is_valid:
        return jsonify({"message": "User verified successfully."}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401
