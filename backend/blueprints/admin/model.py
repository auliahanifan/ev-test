from blueprints import db
from flask_restful import fields
import datetime

# Admin CLASS
class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_username = db.Column(db.String(50), unique=True, nullable=False)
    admin_password = db.Column(db.String(40), nullable=False)
    admin_status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    response_fields = {
        'admin_id': fields.Integer,
        'admin_username': fields.String,
        'admin_password': fields.String,
        'admin_status': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, admin_username, admin_password, admin_status):
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.admin_status = admin_status

    def __repr__(self):
        return '<Admin %r>' % self.id