# filepath: /C:/Users/darob/Documents/Proyectos/apinz/web/api/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_code = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    headoffice = db.Column(db.Text)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    address1 = db.Column(db.Text)
    address2 = db.Column(db.Text)
    address3 = db.Column(db.Text)
    price_category = db.Column(db.Integer, default=1)
    post1 = db.Column(db.Text)
    post2 = db.Column(db.Text)
    post3 = db.Column(db.Text)
    archive = db.Column(db.Text, default='0')
    stopcred = db.Column(db.Boolean, default=False)
    ho_flag = db.Column(db.Boolean, default=False)
    terms_accept = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

class ViewUser(db.Model):
    __tablename__ = 'user_view'  # Name of the view in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_code = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    headoffice = db.Column(db.Text)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    address1 = db.Column(db.Text)
    address2 = db.Column(db.Text)
    address3 = db.Column(db.Text)
    price_category = db.Column(db.Integer, default=1)
    discount = db.Column(db.Numeric)
    post1 = db.Column(db.Text)
    post2 = db.Column(db.Text)
    post3 = db.Column(db.Text)
    archive = db.Column(db.Text, default='0')
    stopcred = db.Column(db.Boolean, default=False)
    ho_flag = db.Column(db.Boolean, default=False)
    terms_accept = db.Column(db.Boolean, default=False)
    

    def __repr__(self):
        return f'<UserView {self.username}>'

class PartApinz(db.Model):
    __tablename__ = 'part_apinz'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    alert = db.Column(db.Text, nullable=False)
    barcode = db.Column(db.String(50), nullable=False)
    price1 = db.Column(db.Numeric(19, 4), nullable=False)
    price2 = db.Column(db.Numeric(19, 4), nullable=False)
    price3 = db.Column(db.Numeric(19, 4), nullable=False)
    price4 = db.Column(db.Numeric(19, 4), nullable=False)
    price5 = db.Column(db.Numeric(19, 4), nullable=False)
    price6 = db.Column(db.Numeric(19, 4), nullable=False)
    make_dbid = db.Column(db.String(2), nullable=False)
    model_dbid = db.Column(db.String(2), nullable=False)
    part_dbid = db.Column(db.String(16), nullable=False)
    model_id = db.Column(db.Integer)
    submodel = db.Column(db.String(40), nullable=False)
    othermodel = db.Column(db.String(50), nullable=False)
    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)
    deleted = db.Column(db.Boolean, nullable=False)
    picture = db.Column(db.SmallInteger, nullable=False)
    part_new = db.Column(db.Boolean)
    special = db.Column(db.Boolean)
    part_old = db.Column(db.Boolean)
    part_perf = db.Column(db.Boolean)
    part_stocklevel = db.Column(db.Integer, nullable=False)
    committedlevel = db.Column(db.Integer, nullable=False)
    showmemberonly = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<PartApinz {self.name}>'
    
class Cart(db.Model):
    __tablename__ = 'cart'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_code = db.Column(db.Text, nullable=False)
    date = db.Column(db.TIMESTAMP)
    ref = db.Column(db.Text)
    tag = db.Column(db.Text)
    add_1 = db.Column(db.Text)
    add_2 = db.Column(db.Text)
    add_3 = db.Column(db.Text)
    attn = db.Column(db.Text)

    def __repr__(self):
        return f'<Cart {self.id}>'
    
class CartItems(db.Model):
    __tablename__ = 'cart_items'  # Name of the table in PostgreSQL
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_stockcode = db.Column(db.Text, nullable=False)
    item_qty = db.Column(db.Float, nullable=False)
    item_reject = db.Column(db.SmallInteger, nullable=False)
    item_part_id = db.Column(db.Integer, nullable=False)
    item_price = db.Column(db.Numeric(19, 4), nullable=False)

    def __repr__(self):
        return f'<CartItems {self.order_id}>'

class PublicCart(db.Model):
    __tablename__ = 'public_cart'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.TIMESTAMP, nullable=False)
    ref = db.Column(db.Text, nullable=False)
    tag = db.Column(db.SmallInteger, nullable=False)
    add_1 = db.Column(db.Text, nullable=False)
    add_2 = db.Column(db.Text, nullable=False)
    add_3 = db.Column(db.Text, nullable=False)
    island = db.Column(db.SmallInteger, nullable=False)
    attn = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    completed = db.Column(db.SmallInteger)
    phone = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<PublicCart {self.id}>'

class PublicCartItems(db.Model):
    __tablename__ = 'public_cart_items'  # Name of the table in PostgreSQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stockcode = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Float, nullable=False)
    reject = db.Column(db.SmallInteger, nullable=False)
    part_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(19, 4), nullable=False)
    freight = db.Column(db.Boolean, nullable=False)
    order_completed = db.Column(db.Boolean, nullable=False)
    cart_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<PublicCartItems {self.id}>'

