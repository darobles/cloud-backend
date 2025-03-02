from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, PartApinz, User
from . import parts_bp

@parts_bp.route('/api/parts', methods=['GET'])
def get_parts():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    print(current_user)
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        price_category = user.price_category
    else:
        price_category = 6  # Assume price_category = 6 for anonymous users
    parts = PartApinz.query.order_by(PartApinz.id.desc()).limit(10).all()
    #parts = PartApinz.query.all()
    parts_list = []
    for part in parts:
        price = getattr(part, f'price{price_category}', part.price1)
        attributes = [{
            
            "Color": "Silver",  # Example attribute
        }]
        attr = jsonify(attributes)
        parts_list.append({
            "id": part.id, 
            "name": part.name, 
            "slug": part.id,#part.part_dbid.lower().replace(' ', '-'),
            "sku": part.part_dbid,
            "images": [
                'https://apinz-web.s3.ap-southeast-2.amazonaws.com/part/TYA4-252G-1+-+800.jpg',
                'assets/images/products/product-2-2.jpg',
            ],            
            "price": price,
            "rating": 5,
            "reviews": 22,
            "availability": 'in-stock',
            "compatibility": [1],
            "attributes": attributes,
            "description": part.description,
            "barcode": part.barcode,
            "price1": part.price1,
            "price2": part.price2,
            "price3": part.price3,
            "price4": part.price4,
            "price5": part.price5,
            "price6": part.price6,
            "make_dbid": part.make_dbid,
            "model_dbid": part.model_dbid,
            "part_dbid": part.part_dbid,
            "model_id": part.model_id,
            "submodel": part.submodel,
            "othermodel": part.othermodel,
            "created": part.created,
            "updated": part.updated,
            "deleted": part.deleted,
            "picture": part.picture,
            "part_new": part.part_new,
            "special": part.special,
            "part_old": part.part_old,
            "part_perf": part.part_perf,
            "part_stocklevel": part.part_stocklevel,
            "committedlevel": part.committedlevel,
            "showmemberonly": part.showmemberonly,

            
            })
    return jsonify(parts_list)
@parts_bp.route('/api/parts/featured/<string:make>', methods=['GET'])
def get_featured_parts(make):
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    print(current_user)
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        price_category = user.price_category
    else:
        price_category = 6  # Assume price_category = 6 for anonymous users
    if make == 'all':
        parts = PartApinz.query.filter(PartApinz.part_new == True).order_by(PartApinz.id.desc()).limit(20).all()
    else:   
        parts = PartApinz.query.filter(PartApinz.part_new == True).filter(PartApinz.make_dbid == make).order_by(PartApinz.id.desc()).limit(20).all()
    parts_list = []
    for part in parts:
        price = getattr(part, f'price{price_category}', part.price1)
        attributes = [{
            "Color": "Silver",  # Example attribute
        }]
        parts_list.append({
            "id": part.id,
            "name": part.name,
            "slug": part.id,
            "sku": part.part_dbid,
            "images": [
                'https://apinz-web.s3.ap-southeast-2.amazonaws.com/part/TYA4-252G-1+-+800.jpg',
                'assets/images/products/product-2-2.jpg',
            ],
            "price": price,
            "rating": 5,
            "reviews": 22,
            "availability": 'in-stock',
            "compatibility": [1],
            "attributes": attributes,
            "description": part.description,
            "barcode": part.barcode,
            "price1": part.price1,
            "price2": part.price2,
            "price3": part.price3,
            "price4": part.price4,
            "price5": part.price5,
            "price6": part.price6,
            "make_dbid": part.make_dbid,
            "model_dbid": part.model_dbid,
            "part_dbid": part.part_dbid,
            "model_id": part.model_id,
            "submodel": part.submodel,
            "othermodel": part.othermodel,
            "created": part.created,
            "updated": part.updated,
            "deleted": part.deleted,
            "picture": part.picture,
            "part_new": part.part_new,
            "special": part.special,
            "part_old": part.part_old,
            "part_perf": part.part_perf,
            "part_stocklevel": part.part_stocklevel,
            "committedlevel": part.committedlevel,
            "showmemberonly": part.showmemberonly,
        })
    return jsonify(parts_list)

@parts_bp.route('/api/parts/featured', methods=['GET'])
def get_featured_parts_old():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    make = request.view_args.get('make')
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        price_category = user.price_category
    else:
        price_category = 6  # Assume price_category = 6 for anonymous users
    parts = PartApinz.query.filter(PartApinz.part_new == True).filter(PartApinz.make_dbid == make).order_by(PartApinz.id.desc()).limit(20).all()
    #parts = PartApinz.query.all()
    parts_list = []
    for part in parts:
        price = getattr(part, f'price{price_category}', part.price1)
        attributes = [{
            
            "Color": "Silver",  # Example attribute
        }]
        attr = jsonify(attributes)
        parts_list.append({
            "id": part.id, 
            "name": part.name, 
            "slug": part.id,#part.part_dbid.lower().replace(' ', '-'),
            "sku": part.part_dbid,
            "images": [
                'https://apinz-web.s3.ap-southeast-2.amazonaws.com/part/TYA4-252G-1+-+800.jpg',
                'assets/images/products/product-2-2.jpg',
            ],            
            "price": price,
            "rating": 5,
            "reviews": 22,
            "availability": 'in-stock',
            "compatibility": [1],
            "attributes": attributes,
            "description": part.description,
            "barcode": part.barcode,
            "price1": part.price1,
            "price2": part.price2,
            "price3": part.price3,
            "price4": part.price4,
            "price5": part.price5,
            "price6": part.price6,
            "make_dbid": part.make_dbid,
            "model_dbid": part.model_dbid,
            "part_dbid": part.part_dbid,
            "model_id": part.model_id,
            "submodel": part.submodel,
            "othermodel": part.othermodel,
            "created": part.created,
            "updated": part.updated,
            "deleted": part.deleted,
            "picture": part.picture,
            "part_new": part.part_new,
            "special": part.special,
            "part_old": part.part_old,
            "part_perf": part.part_perf,
            "part_stocklevel": part.part_stocklevel,
            "committedlevel": part.committedlevel,
            "showmemberonly": part.showmemberonly,

            
            })
    return jsonify(parts_list)

@parts_bp.route('/api/parts/<int:part_id>', methods=['GET'])
def get_part(part_id):
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        price_category = user.price_category
    else:
        price_category = 6  # Assume price_category = 6 for anonymous users

    part = PartApinz.query.get(part_id)
    if part is None:
        return jsonify({"error": "Part not found"}), 404

    price = getattr(part, f'price{price_category}', part.price1)
    attributes = [{
            
            "Color": "Silver",  # Example attribute
        }]
    part_data = {
        "id": part.id, 
        "name": part.name, 
        "slug": part.part_dbid.lower().replace(' ', '-'),#part.part_dbid.lower().replace(' ', '-'),
        "sku": part.part_dbid,
        "images": [
            'https://apinz-web.s3.ap-southeast-2.amazonaws.com/part/TYA4-252G-1+-+800.jpg',
            'assets/images/products/product-2-2.jpg',
        ],            
        "price": price,
        "rating": 5,
        "reviews": 22,
        "availability": 'in-stock',
        "compatibility": [1],
        "attributes": attributes,
        "description": part.description,
        "barcode": part.barcode,
        "price1": part.price1,
        "price2": part.price2,
        "price3": part.price3,
        "price4": part.price4,
        "price5": part.price5,
        "price6": part.price6,
        "make_dbid": part.make_dbid,
        "model_dbid": part.model_dbid,
        "part_dbid": part.part_dbid,
        "model_id": part.model_id,
        "submodel": part.submodel,
        "othermodel": part.othermodel,
        "created": part.created,
        "updated": part.updated,
        "deleted": part.deleted,
        "picture": part.picture,
        "part_new": part.part_new,
        "special": part.special,
        "part_old": part.part_old,
        "part_perf": part.part_perf,
        "part_stocklevel": part.part_stocklevel,
        "committedlevel": part.committedlevel,
        "showmemberonly": part.showmemberonly,
    }
    return jsonify(part_data)

@parts_bp.route('/api/parts', methods=['POST'])
@jwt_required()
def add_part():
    data = request.get_json()
    new_part = PartApinz(
        name=data.get('name'),
        description=data.get('description'),
        alert=data.get('alert'),
        barcode=data.get('barcode'),
        price1=data.get('price1'),
        price2=data.get('price2'),
        price3=data.get('price3'),
        price4=data.get('price4'),
        price5=data.get('price5'),
        price6=data.get('price6'),
        make_dbid=data.get('make_dbid'),
        model_dbid=data.get('model_dbid'),
        part_dbid=data.get('part_dbid'),
        model_id=data.get('model_id'),
        submodel=data.get('submodel'),
        othermodel=data.get('othermodel'),
        created=data.get('created'),
        updated=data.get('updated'),
        deleted=data.get('deleted'),
        picture=data.get('picture'),
        part_new=data.get('part_new'),
        special=data.get('special'),
        part_old=data.get('part_old'),
        part_perf=data.get('part_perf'),
        part_stocklevel=data.get('part_stocklevel'),
        committedlevel=data.get('committedlevel'),
        showmemberonly=data.get('showmemberonly')
    )
    db.session.add(new_part)
    db.session.commit()
    return jsonify({"msg": "Part added successfully"}), 201

@parts_bp.route('/api/parts/<int:part_id>', methods=['PUT'])
@jwt_required()
def update_part(part_id):
    part = PartApinz.query.get(part_id)
    if part is None:
        return jsonify({"error": "Part not found"}), 404
    data = request.get_json()
    part.name = data.get('name', part.name)
    part.description = data.get('description', part.description)
    part.alert = data.get('alert', part.alert)
    part.barcode = data.get('barcode', part.barcode)
    part.price1 = data.get('price1', part.price1)
    part.price2 = data.get('price2', part.price2)
    part.price3 = data.get('price3', part.price3)
    part.price4 = data.get('price4', part.price4)
    part.price5 = data.get('price5', part.price5)
    part.price6 = data.get('price6', part.price6)
    part.make_dbid = data.get('make_dbid', part.make_dbid)
    part.model_dbid = data.get('model_dbid', part.model_dbid)
    part.part_dbid = data.get('part_dbid', part.part_dbid)
    part.model_id = data.get('model_id', part.model_id)
    part.submodel = data.get('submodel', part.submodel)
    part.othermodel = data.get('othermodel', part.othermodel)
    part.created = data.get('created', part.created)
    part.updated = data.get('updated', part.updated)
    part.deleted = data.get('deleted', part.deleted)
    part.picture = data.get('picture', part.picture)
    part.part_new = data.get('part_new', part.part_new)
    part.special = data.get('special', part.special)
    part.part_old = data.get('part_old', part.part_old)
    part.part_perf = data.get('part_perf', part.part_perf)
    part.part_stocklevel = data.get('part_stocklevel', part.part_stocklevel)
    part.committedlevel = data.get('committedlevel', part.committedlevel)
    part.showmemberonly = data.get('showmemberonly', part.showmemberonly)
    db.session.commit()
    return jsonify({"msg": "Part updated successfully"}), 200

@parts_bp.route('/api/parts/<int:part_id>', methods=['DELETE'])
@jwt_required()
def delete_part(part_id):
    part = PartApinz.query.get(part_id)
    if part is None:
        return jsonify({"error": "Part not found"}), 404
    db.session.delete(part)
    db.session.commit()
    return jsonify({"msg": "Part deleted successfully"}), 200

