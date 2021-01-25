from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
import json
from .model import UserDetails
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app
import datetime

bp_user_details = Blueprint('user_detail', __name__)
api_user_details = Api(bp_user_details)

#######################
# Using flask-restful
#######################

class UserDetailsResource(Resource):

    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    # method to get user detail by user_id
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = UserDetails.query.get(claims['user_id'])
        if qry is not None:
            return marshal(qry, UserDetails.response_fields), 200
        return {'status':'NOT_FOUND'}, 400

    # method to post new user detail
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location = 'json', required = True)
        parser.add_argument('address', location = 'json', required = True)
        parser.add_argument('sex', location = 'json', required = True)
        parser.add_argument('phone', location = 'json', required = True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('city', location='json', required=True)
        parser.add_argument('district', location='json', required=True)
        parser.add_argument('zip_code', location='json', required=True)

        # to get data from body
        data = parser.parse_args()
        # to get data from jwt_claims
        claims = get_jwt_claims()

        user_details = UserDetails(
            claims['user_id'], 
            data['full_name'], 
            data['sex'], 
            data['phone'],
            data['address'],
            data['province'],
            data['city'],
            data['district'],
            data['zip_code']
        )

        db.session.add(user_details)
        db.session.commit()

        app.logger.debug('DEBUG: %s', user_details)

        return marshal(user_details, UserDetails.response_fields), 200, {'Content-Type':'application/json'}

    # method to edit user details
    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        qry = UserDetails.query.get(claims['user_id'])

        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location = 'json', default = qry.full_name)
        parser.add_argument('address', location = 'json', default = qry.address)
        parser.add_argument('sex', location = 'json', default = qry.sex)
        parser.add_argument('phone', location = 'json', default = qry.phone)
        parser.add_argument('province', location='json', default=qry.province)
        parser.add_argument('city', location='json', default=qry.city)
        parser.add_argument('district', location='json', default=qry.district)
        parser.add_argument('zip_code', location='json', default=qry.zip_code)
        data = parser.parse_args()
        

        if qry is None:
            return {'status':'USER_NOT_FOUND'}, 400

        # to check if this is user's own detail
        if qry.user_id != int(claims['user_id']):
            return {'status':'INVALID_ACTION'}, 400
        
        qry.full_name = data['full_name']
        qry.address = data['address']
        qry.sex = data['sex']
        qry.phone = data['phone']
        qry.province = data['province']
        qry.city = data['city']
        qry.district = data['district']
        qry.zip_code = data['zip_code']
        qry.updated_at = datetime.datetime.now()

        db.session.commit()

        return marshal(qry, UserDetails.response_fields), 200
    

    # method to delete user by id
    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        user_id = int(claims['user_id'])
        qry = UserDetails.query.get(user_id)
        if qry is not None:

            db.session.delete(qry)
            db.session.commit()

            return {'status':'DELETED'}, 200


       
        
api_user_details.add_resource(UserDetailsResource, '', '/<user_id>')