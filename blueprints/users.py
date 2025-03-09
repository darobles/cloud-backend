# filepath: /C:/Users/darob/Documents/Proyectos/apinz/web/api/blueprints/users.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from models import db, ViewUser, User
from . import users_bp
import jwt
from flask_cors import CORS


CORS(users_bp, supports_credentials=True)

@users_bp.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, DELETE, PUT'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@users_bp.route('/api/users', methods=['GET'])
def get_users():    
    users = ViewUser.query.all()
    users_list = [user.to_dict() for user in users]  # Convert each user to a dictionary
    return users_list, 201

@users_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        username = data.get('username'),
        name = data.get('name'),
        email = data.get('email'),
        address = data.get('address'),
        city = data.get('city'),
        country =  data.get('country'),
        post =  data.get('post'),
        role_id =  data.get('role_id'),
        password = generate_password_hash(data.get('password'))
    )
    db.session.add(user)
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
    print(user)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    username = user.username
    data = request.get_json()
    user.name = data.get('name', user.name)
    [print(data.get(key)) for key in data.keys()]
    user.email = data.get('email', user.email)
    user.address = data.get('address', user.address)
    user.city = data.get('city', user.city)
    user.country =  data.get('country', user.country)
    user.post =  data.get('post', user.post)
    user.role_id =  data.get('role_id', user.role_id)
    user.password = user.password 
    if data.get('password') != user.password:
        user.password = generate_password_hash(data.get('password'))
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
    user_data = user.to_dict()

    return jsonify(user_data), 200