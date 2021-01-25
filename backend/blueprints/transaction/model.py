from blueprints import db
from flask_restful import fields
import datetime

class Transaction(db.Model):
    __tablename__ = "transaction"
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    total_price = db.Column(db.Integer, default=0)
    full_name = db.Column(db.String(40), nullable=False)
    handphone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    district = db.Column(db.String(40), nullable=False)
    zip_code = db.Column(db.String(6), nullable=False)
    note =db.Column(db.String(1000), nullable=True)
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    response_fields = {
        'transaction_id' : fields.Integer,
        'user_id' : fields.Integer,
        'total_price' : fields.Integer,
        'full_name': fields.String,
        'handphone': fields.String,
        'address': fields.String,
        'province': fields.String,
        'city': fields.String,
        'district': fields.String,
        'zip_code': fields.String,
        'note' : fields.String,        
        'status': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, user_id, total_price,full_name, handphone, address, province, city, district, zip_code, note, status):
        self.user_id = user_id
        self.full_name = full_name
        self.handphone = handphone
        self.address = address
        self.province = province
        self.city = city
        self.district = district
        self.zip_code = zip_code
        self.note = note
        self.total_price = total_price
        self.status = status
    
    def __repr__(self):
        return '<Transaction %r>' % self.transaction_id
