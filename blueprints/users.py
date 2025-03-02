# filepath: /C:/Users/darob/Documents/Proyectos/apinz/web/api/blueprints/users.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from models import db, ViewUser, User
from . import users_bp
import jwt

@users_bp.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@users_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200

@users_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username:
        user.username = username
    if password:
        user.password = generate_password_hash(password)
    db.session.commit()
    return jsonify({"msg": "User updated successfully"}), 200

@users_bp.route('/api/users/info', methods=['GET'])
@jwt_required()
def get_user():
    token = request.headers.get('Authorization').split(' ')[1]
    payload = jwt.decode(token, 'apinz2025', algorithms=['HS256'])
    user_id = payload['sub']
    user = User.query.filter_by(username=user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user_data = {
        "username": user.username,
        "email": user.email,
        "phone": '12312313132',
        "firstName": user.name,
        "lastName": user.headoffice,
        "avatar": '//www.gravatar.com/avatar/bde30b7dd579b3c9773f80132523b4c3?d=mp&s=88'
        }

    return jsonify(user_data), 200
    return jsonify({"msg": "User updated successfully"}), 200