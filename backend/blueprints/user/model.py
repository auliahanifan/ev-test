from blueprints import db
from flask_restful import fields
import datetime

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    response_fields = {
        'user_id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'email': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    jwt_response_fields = {
        'user_id': fields.String,
        'username': fields.String
    }

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.user_id
