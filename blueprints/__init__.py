# filepath: /C:/Users/darob/Documents/Proyectos/apinz/web/api/blueprints/__init__.py
from flask import Blueprint

users_bp = Blueprint('users', __name__)
parts_bp = Blueprint('parts', __name__)
cart_bp = Blueprint('cart', __name__)

from . import users, parts, cart