from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, Product, User, ProductView
from . import products_bp
import json
from decimal import Decimal
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
import configparser
import boto3
import mimetypes

CORS(products_bp, supports_credentials=True)

def get_azure_config():
    config = configparser.ConfigParser()
    config.read('config/azure.ini')
    return {
        'connection_string': config['azure']['CONNECTION_STRING'],
        'container_name': config['azure']['CONTAINER_NAME']
    }

def get_aws_config():
    config = configparser.ConfigParser()
    config.read('config/aws.ini')
    return {
        'bucket_name': config['aws']['BUCKET_NAME'],
    }

@products_bp.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, DELETE, PUT'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# ✅ Explicitly handle preflight requests
@products_bp.route('/api/products/<int:product_id>', methods=['OPTIONS'])
def options_product(product_id):
    response = jsonify({'message': 'CORS preflight successful'})
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, DELETE, PUT'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@products_bp.route('/api/products', methods=['GET'])
def get_products():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    '''
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
    '''
    products = ProductView.query.all()
    product = [p.to_dict() for p in products]
    print(len(products))
    return product, 200

@products_bp.route('/api/products/test', methods=['GET'])
def get_products_test():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    print(current_user)
    '''
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
    '''        
    products = ProductView.query.all()
    product = [p.to_dict() for p in products]
    return product, 200

@products_bp.route('/api/products/<int:product_id>', methods=['GET', 'OPTIONS'])
def get_product(product_id):
    product = ProductView.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@products_bp.route('/api/products', methods=['POST'])
def create_product():
    data = request.form.to_dict()
    file = request.files.get('image')
    image_url = None
    print(data)
    if file:
        print(file.filename)
        image_url = uploadfile(file)
    try:
        product = Product(
            name=data['name'],
            price=data['price'],
            image=image_url,
            category_id=data['category_id'],
            description=data['description'],
            stock=int(data['stock'])
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

@products_bp.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    print(product_id)
    product = Product.query.get_or_404(product_id)
    data = request.form.to_dict()
    file = request.files.get('image')
    image_url = None
    if file:
        print(file.filename)
        image_url = uploadfile(file)
    try:
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.image = data.get('image', product.image)
        product.category_id = data.get('category_id', product.category_id)
        product.description = data.get('description', product.description)
        product.stock = int(data.get('stock', product.stock))
        if image_url:
            product.image = image_url
        db.session.commit()
        product_return = ProductView.query.get_or_404(product_id)
        return jsonify(product_return.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

@products_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

def uploadfileazure(file):
    azure_config = get_azure_config()
    blob_service_client = BlobServiceClient.from_connection_string(azure_config['connection_string'])
    container_client = blob_service_client.get_container_client(azure_config['container_name'])
    content_type = file.content_type if hasattr(file, "content_type") else "image/jpeg"
    content_settings = ContentSettings(content_type=content_type)
    blob_client = container_client.get_blob_client(file.filename)
    file_data = file.read()
    blob_client.upload_blob(file_data, overwrite=True, content_settings=content_settings)
    file_url = blob_client.url
    print(f"✅ File uploaded: {file_url}")
    return file_url

def uploadfile(file):
    aws_config = get_aws_config()
    s3_client = boto3.client(
        's3',
        code1='',
        code2=''
    )
    try:
        bucket_name = aws_config['bucket_name']
        content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'
        
        # Upload directly from file object
        s3_client.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                'ContentType': content_type
            }
        )
        
        region = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        public_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{file.filename}"
        print(f"Public URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"Failed to upload {file}: {e}")
        return None