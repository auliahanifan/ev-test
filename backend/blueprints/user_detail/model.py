from blueprints import db
from flask_restful import fields
import datetime

class UserDetails(db.Model):
    __tablename__ = "user_details"
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key = True, nullable = False)
    full_name = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    district = db.Column(db.String(40), nullable=False)
    zip_code = db.Column(db.String(6), nullable=False)
    sex = db.Column(db.String(10), nullable = False)
    phone = db.Column(db.String(20), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    response_fields = {
        'user_id' : fields.Integer,
        'full_name' : fields.String,
        'sex' : fields.String,
        'phone' : fields.String,
        'address' : fields.String,
        'province': fields.String,
        'city': fields.String,
        'district': fields.String,
        'zip_code': fields.String
    }

    def __init__(self, user_id, full_name, sex, phone, address, province, city, district, zip_code):
        self.user_id = user_id
        self.full_name = full_name
        self.address = address
        self.sex = sex
        self.phone = phone
        self.province = province
        self.city = city
        self.district = district
        self.zip_code = zip_code
    
    def __repr__(self):
        return '<UserDetails %r>' % self.user_id