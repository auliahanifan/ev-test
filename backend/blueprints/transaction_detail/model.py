from blueprints import db
from flask_restful import fields
import datetime

class TransactionDetails(db.Model):
    __tablename__ = "transaction_details"
    transaction_detail_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    transaction_id = db.Column(db.Integer,  nullable = False)
    product_id = db.Column(db.Integer,  nullable = False)
    product_name = db.Column(db.String(100), nullable = False)
    quantity = db.Column(db.Integer, nullable = False, default = 1)
    total_price = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    response_fields = {
        'transaction_id' : fields.Integer,
        'product_id' : fields.Integer,
        'product_name' : fields.String,
        'quantity' : fields.Integer,
        'total_price' : fields.Integer,
        'created_at': fields.DateTime
    }

    def __init__(self, transaction_id, product_id, product_name, quantity, total_price):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
    
    def __repr__(self):
        return '<TransactionDetails %r>' % self.transaction_id