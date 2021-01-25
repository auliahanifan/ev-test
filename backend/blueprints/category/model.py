from blueprints import db
from flask_restful import fields
import datetime

class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False)
    category_description = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    response_fields = {
        'category_id': fields.Integer,
        'category_name': fields.String,
        'category_description': fields.String,
        'created_at': fields.DateTime,
        'created_at': fields.DateTime
    }

    def __init__(self, category_name, category_description):
        self.category_name = category_name
        self.category_description = category_description

    def __repr__(self):
        return '<User %r>' % self.category_id