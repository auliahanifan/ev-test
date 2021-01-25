from blueprints import db
from flask_restful import fields
import datetime 

class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    admin_id = db.Column(db.Integer, nullable = False)
    product_name = db.Column(db.String(100), nullable = False)
    product_stock = db.Column(db.Integer, default = 1)
    product_price = db.Column(db.Integer, nullable = False)
    product_description = db.Column(db.String(1000), nullable=False)
    product_image_url = db.Column(db.String(1000), nullable=False)
    product_weight = db.Column(db.String(1000), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    response_fields = {
        'product_id' : fields.Integer,
        'admin_id' : fields.Integer,
        'category_id' : fields.Integer,
        'product_name' : fields.String,
        'product_stock' : fields.Integer,
        'product_price' : fields.Integer,
        'product_weight' : fields.Integer,
        'product_image_url' : fields.String,
        'product_description' : fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, admin_id, category_id, product_name, product_stock, product_price, product_weight, product_image_url, product_description):
        self.admin_id = admin_id
        self.category_id = category_id
        self.product_name = product_name
        self.product_stock = product_stock
        self.product_price = product_price
        self.product_weight = product_weight
        self.product_image_url = product_image_url
        self.product_description = product_description
    
    def __repr__(self):
        return '<Product %r>' % self.product_id