from flask import jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, Cart, CartItems,Category, CartItemsView, Product, User, PublicCart, PublicCartItems
from . import cart_bp
import datetime
import uuid

def get_or_create_public_cart():    
    if 'public_cart_id' not in session:
        print("Not found public_cart_id")
        public_cart = PublicCart(
            date=datetime.datetime.utcnow(),
            ref=str(uuid.uuid4()),  # Generate a unique reference for the cart
            add_1='',
            add_2='',
            add_3='',
            email='',
            notes='',
            phone=''
        )
        db.session.add(public_cart)
        db.session.commit()
        session['public_cart_id'] = public_cart.id
    else:
        print("Found public_cart_id")
        public_cart = PublicCart.query.get(session['public_cart_id'])
    return public_cart

@cart_bp.route('/api/cart', methods=['POST'])
def add_to_cart():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Part not found"}), 404

    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(user_id=user.id).first()
        if not cart:
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()     
        cart_item = CartItems.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItems(
                cart_id=cart.id,
                quantity=quantity,
                product_id=product_id,
                price=product.price
            )
            db.session.add(cart_item)
    else:
        public_cart = get_or_create_public_cart()
        cart_item = PublicCartItems.query.filter_by(product_id=product_id, public_cart_id=public_cart.id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = PublicCartItems(
                public_cart_id=public_cart.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price  # Default price, you can adjust based on user category if needed
            )
            db.session.add(cart_item)
    db.session.commit()
    return jsonify({"msg": "Item added to cart"}), 201

@cart_bp.route('/api/cart', methods=['GET'])
def view_cart():
    print('call get')
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    print(current_user)
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(user_id=user.id).first()
        if not cart:
            return jsonify([]), 404

        cart_items = CartItemsView.query.filter_by(cart_id=cart.id).all()
        items = []
        for item in cart_items:
            productview = Product.query.get(item.id)
            items.append({
                "quantity": item.quantity,
                "product": {
                    "id": productview.id,
                    "name": productview.name,
                    "price": productview.price,
                    "image": productview.image,
                    "category": item.category,
                    "category_id": productview.category_id,
                    "description": productview.description
                }
            })
    else:
        if 'public_cart_id' not in session:
            return jsonify([]), 200
        public_cart = PublicCart.query.get(session['public_cart_id'])
        if not public_cart:
            return jsonify([]), 200

        cart_items = PublicCartItems.query.filter_by(public_cart_id=public_cart.id).all()
        items = []
        for item in cart_items:
            product = Product.query.get(item.id)
            category = Category.query.get(product.category_id)
            items.append({
                "quantity": item.quantity,
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "image": product.image,
                    "category": category.name,
                    "category_id": product.category_id,
                    "description": product.description
                }
            })
    return jsonify(items)

@cart_bp.route('/api/cart/<int:product_id>', methods=['PUT'])
def update_cart_item(product_id):
    print('call put')
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    print(current_user)
    data = request.get_json()
    quantity = data.get('quantity')
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        print(user)
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(user_id=user.id).first()
        if not cart:
            return jsonify({"error": "Cart not found"}), 404
        cart_item = CartItems.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        cart_item.quantity = quantity
    else:
        if 'public_cart_id' not in session:
            return jsonify({"error": "Cart not found"}), 404

        public_cart = PublicCart.query.get(session['public_cart_id'])
        if not public_cart:
            return jsonify({"error": "Cart not found"}), 404

        cart_item = PublicCartItems.query.filter_by(product_id=product_id, public_cart_id=public_cart.id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        cart_item.quantity = quantity
    db.session.commit()
    return jsonify({"msg": "Cart item updated"}), 200

@cart_bp.route('/api/cart/<int:product_id>', methods=['DELETE'])
def remove_cart_item(product_id):
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()

    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(user_id=user.id).first()
        if not cart:
            return jsonify({"error": "Cart not found"}), 404

        cart_item = CartItems.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        db.session.delete(cart_item)
    else:
        if 'public_cart_id' not in session:
            return jsonify({"error": "Cart not found"}), 404

        public_cart = PublicCart.query.get(session['public_cart_id'])
        if not public_cart:
            return jsonify({"error": "Cart not found"}), 404

        cart_item = PublicCartItems.query.filter_by(product_id=product_id, public_cart_id=public_cart.id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"msg": "Cart item removed"}), 200

@cart_bp.route('/api/process', methods=['DELETE'])
def process():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(user_id=user.id).first()
        if not cart:
            return jsonify([]), 404
        cart_items = CartItems.query.filter_by(cart_id=cart.id).all()
        for item in cart_items:
            db.session.delete(item)
        db.session.commit()
    else:
        if 'public_cart_id' not in session:
            return jsonify({"error": "Cart not found"}), 404

        public_cart = PublicCart.query.get(session['public_cart_id'])
        if not public_cart:
            return jsonify({"error": "Cart not found"}), 404

        cart_item = PublicCartItems.query.filter_by(product_id=product_id, public_cart_id=public_cart.id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"msg": "Cart item removed"}), 200