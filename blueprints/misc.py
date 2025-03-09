from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, Category
from . import misc_bp
import json

@misc_bp.route('/api/categories', methods=['GET'])
def get_categories():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    query = Category.query.all()
    categories = [p.to_dict() for p in query]
    return categories, 200