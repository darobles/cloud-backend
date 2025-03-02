from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User  # Ensure models.py contains the User model and db instance
from blueprints import users_bp, parts_bp, cart_bp
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Dota0345!@localhost:5433/apinz_website'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'apinz2025'  # Change this to a random secret key
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session management

db.init_app(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)  # Enable CORS with credentials

app.register_blueprint(users_bp)
app.register_blueprint(parts_bp)
app.register_blueprint(cart_bp)

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt_identity()
    # Here you can add the token to a blacklist or perform other logout operations
    return jsonify({"msg": "Successfully logged out"}), 200

if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()*/
    app.run(host='0.0.0.0', port='5000')