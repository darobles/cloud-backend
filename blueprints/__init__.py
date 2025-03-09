# filepath: /C:/Users/darob/Documents/Proyectos/apinz/web/api/blueprints/__init__.py
from flask import Blueprint

users_bp = Blueprint('users', __name__)
cart_bp = Blueprint('cart', __name__)
products_bp = Blueprint('products', __name__)
misc_bp = Blueprint('misc', __name__)

from . import users, cart, products, misc