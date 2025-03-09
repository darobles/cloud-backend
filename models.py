# filepath: /C:/Users/darob/Documents/Proyectos/apinz/web/api/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)
    post = db.Column(db.Text)
    role_id = db.Column(db.Integer)
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    def __repr__(self):
        return f'<User {self.username}>'

class ViewUser(db.Model):
    __tablename__ = 'users_view'  # Name of the view in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)
    post = db.Column(db.Text)
    role = db.Column(db.Text)
    role_id = db.Column(db.Integer)
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    def __repr__(self):
        return f'<UserView {self.username}>'

class ProductView(db.Model):
    __tablename__ = 'products_view'
    __table_args__ = (
        db.CheckConstraint('stock >= 0', name='check_stock_non_negative'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer)
    category = db.Column(db.Text)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    def __repr__(self):
        return f'<ProductView {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    def __repr__(self):
        return f'<Product {self.name}>'


class Cart(db.Model):
    __tablename__ = 'cart'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Text, nullable=False)
    date = db.Column(db.TIMESTAMP)
    def __repr__(self):
        return f'<Cart {self.id}>'
    
class CartItems(db.Model):
    __tablename__ = 'cart_items'  # Name of the table in PostgreSQL
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cart_id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Numeric(19, 4), nullable=False)

    def __repr__(self):
        return f'<CartItems {self.order_id}>'


class CartItemsView(db.Model):
    __tablename__ = 'cartitems_view'  # Name of the table in PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text)
    category_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f'<CartItemsView {self.order_id}>'

class PublicCart(db.Model):
    __tablename__ = 'public_cart'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.TIMESTAMP, nullable=False)
    ref = db.Column(db.Text, nullable=False)
    add_1 = db.Column(db.Text, nullable=False)
    add_2 = db.Column(db.Text, nullable=False)
    add_3 = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<PublicCart {self.id}>'

class PublicCartItems(db.Model):
    __tablename__ = 'public_cart_items'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Numeric(19, 4), nullable=False)
    public_cart_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<PublicCartItems {self.id}>'

class Category(db.Model):
    __tablename__ = 'categories'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    def __repr__(self):
        return f'<Category {self.id}>'

