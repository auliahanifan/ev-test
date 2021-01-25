from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
import json
from .model import User
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app
import datetime

bp_user = Blueprint('user', __name__)
api_user = Api(bp_user)

class UserResource(Resource):

    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    # method get user by id
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = int(claims['user_id'])
        qry = User.query.get(user_id)
        if qry is not None:
            return marshal(qry, User.response_fields), 200
        return {'status':'USER_NOT_FOUND'}, 400
    
    # method to register new user
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        data = parser.parse_args()

        user = User(data['username'], data['password'], data['email'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG: %s', user)

        return marshal(user, User.response_fields), 200, {'Content-Type':'application/json'}

    # method to delete user by id
    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        user_id = int(claims['user_id'])
        qry = User.query.get(user_id)
        if qry is not None:

            db.session.delete(qry)
            db.session.commit()

            return {'status':'DELETED'}, 200

    # method to edit user by id
    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        user_id = int(claims['user_id'])
        qry = User.query.get(user_id)

        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        data = parser.parse_args()
        # claims = get_jwt_claims()
 
        if qry is None:
            return {'status':'USER_NOT_FOUND'}, 400
        
        # to check if the user is the correct owner of the item
        # if qry.user_id != int(claims['user_id']):
        #     return {'status':'INVALID_ACTION'}, 400
        
        qry.username = data['username']
        qry.password = data['password']
        qry.email = data['email']
        qry.updated_at = datetime.datetime.now()

        db.session.commit()

        return marshal(qry, User.response_fields), 200

api_user.add_resource(UserResource, '', '/<user_id>')