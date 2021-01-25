from blueprints import db
from flask_restful import fields
import datetime

class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable = False)
    qty = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    response_fields = {
        'cart_id': fields.Integer,
        'user_id': fields.Integer,
        'product_id': fields.Integer,
        'product_name': fields.String,
        'qty': fields.Integer,
        'price': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, user_id, product_id, product_name, qty, price):
        self.user_id = user_id
        self.product_id = product_id
        self.product_name = product_name
        self.qty = qty
        self.price = price

    def __repr__(self):
        return '<Cart %r>' % self.cart_id
