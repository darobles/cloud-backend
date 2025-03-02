from flask import jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, Cart, CartItems, PartApinz, User, PublicCart, PublicCartItems
from . import cart_bp
import datetime
import uuid

def get_or_create_public_cart():    
    if 'public_cart_id' not in session:
        print("Not found public_cart_id")
        public_cart = PublicCart(
            date=datetime.datetime.utcnow(),
            ref=str(uuid.uuid4()),  # Generate a unique reference for the cart
            tag=0,
            add_1='',
            add_2='',
            add_3='',
            island=0,
            attn='',
            email='',
            notes='',
            password='',
            completed=0,
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
    part_id = data.get('part_id')
    quantity = data.get('quantity')

    part = PartApinz.query.get(part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(cust_code=user.cust_code).first()
        if not cart:
            cart = Cart(cust_code=user.cust_code)
            db.session.add(cart)
            db.session.commit()     
        cart_item = CartItems.query.filter_by(order_id=cart.id, item_part_id=part_id).first()
        if cart_item:
            cart_item.item_qty += quantity
        else:
            cart_item = CartItems(
                order_id=cart.id,
                item_stockcode=part.part_dbid,
                item_qty=quantity,
                item_reject=0,
                item_part_id=part_id,
                item_price=getattr(part, f'price{user.price_category}', part.price1)
            )
            db.session.add(cart_item)
    else:
        public_cart = get_or_create_public_cart()
        cart_item = PublicCartItems.query.filter_by(part_id=part_id, cart_id=public_cart.id).first()
        if cart_item:
            cart_item.qty += quantity
        else:
            cart_item = PublicCartItems(
                cart_id=public_cart.id,
                stockcode=part.part_dbid,
                qty=quantity,
                reject=0,
                part_id=part_id,
                price=part.price1,  # Default price, you can adjust based on user category if needed
                freight=False,
                order_completed=False
            )
            db.session.add(cart_item)
    db.session.commit()
    return jsonify({"msg": "Item added to cart"}), 201

@cart_bp.route('/api/cart', methods=['GET'])
def view_cart():
    print('call get')
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()

    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(cust_code=user.cust_code).first()
        if not cart:
            return jsonify({"error": "Cart is empty"}), 404

        cart_items = CartItems.query.filter_by(order_id=cart.id).all()
        items = []
        for item in cart_items:
            part = PartApinz.query.get(item.item_part_id)
            items.append({
                "part_id": item.item_part_id,
                "name": part.name,
                "quantity": item.item_qty,
                "price": item.item_price
            })
    else:
        if 'public_cart_id' not in session:
            return jsonify({"error": "Cart is empty"}), 404
        public_cart = PublicCart.query.get(session['public_cart_id'])
        if not public_cart:
            return jsonify({"error": "Cart not found"}), 404

        cart_items = PublicCartItems.query.filter_by(cart_id=public_cart.id).all()
        items = []
        for item in cart_items:
            part = PartApinz.query.get(item.part_id)
            items.append({
                "part_id": item.part_id,
                "name": part.name,
                "quantity": item.qty,
                "price": item.price
            })
    return jsonify(items)

@cart_bp.route('/api/cart/<int:part_id>', methods=['PUT'])
def update_cart_item(part_id):
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    data = request.get_json()
    quantity = data.get('quantity')

    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(cust_code=user.cust_code).first()
        if not cart:
            return jsonify({"error": "Cart not found"}), 404
        cart_item = CartItems.query.filter_by(order_id=cart.id, item_part_id=part_id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        cart_item.item_qty = quantity
    else:
        if 'public_cart_id' not in session:
            return jsonify({"error": "Cart not found"}), 404

        public_cart = PublicCart.query.get(session['public_cart_id'])
        if not public_cart:
            return jsonify({"error": "Cart not found"}), 404

        cart_item = PublicCartItems.query.filter_by(part_id=part_id, cart_id=public_cart.id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        cart_item.qty = quantity
    db.session.commit()
    return jsonify({"msg": "Cart item updated"}), 200

@cart_bp.route('/api/cart/<int:part_id>', methods=['DELETE'])
def remove_cart_item(part_id):
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()

    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = Cart.query.filter_by(cust_code=user.cust_code).first()
        if not cart:
            return jsonify({"error": "Cart not found"}), 404

        cart_item = CartItems.query.filter_by(cart_id=cart.id, item_part_id=part_id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        db.session.delete(cart_item)
    else:
        if 'public_cart_id' not in session:
            return jsonify({"error": "Cart not found"}), 404

        public_cart = PublicCart.query.get(session['public_cart_id'])
        if not public_cart:
            return jsonify({"error": "Cart not found"}), 404

        cart_item = PublicCartItems.query.filter_by(part_id=part_id, cart_id=public_cart.id).first()
        if not cart_item:
            return jsonify({"error": "Item not found in cart"}), 404

        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"msg": "Cart item removed"}), 200