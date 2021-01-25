from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from ..user.model import User
from ..admin.model import Admin

bp_auth = Blueprint('auth', __name__)
api_auth = Api(bp_auth)

class CreateTokenUserResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    # token for login
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required = True)
        parser.add_argument('password', location='json', required = True)
        data = parser.parse_args()

        # crosscheck database by filtering both username and password
        user_query = User.query.filter_by(username = data['username']).filter_by(password = data['password']).first()
        # response field to be inserted into jwt_claims
        user_data = marshal(user_query, User.jwt_response_fields)

        if user_query is not None:
            token = create_access_token(identity = user_query.username ,user_claims = user_data)
        else:
            return {'status':'ACCES DENIED : UNAUTHORIZED', 'message':'invalid username or password'}, 401

        return {
            'token':token,   
            'status':'success'
        }, 200

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {'claims': claims}, 200

class RefreshTokenResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    # method to refresh token
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity = current_user)
        return {'token':token, 'identity':current_user}, 200

class CreateTokenAdminResource(Resource):


    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    # token for login
    def post(self):
    ## Create token
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json', required=True)
        parser.add_argument('password', type=str, location='json', required= True)
        args = parser.parse_args()

        qry = Admin.query

        qry = qry.filter_by(admin_username=args['username'])
        qry = qry.filter_by(admin_password=args['password']).first()
        
        if qry is not None:
            admin_data= marshal(qry, Admin.response_fields)
            admin_data.pop("admin_password")
            token = create_access_token(identity=args['username'], user_claims=admin_data)
        else:
            return {'status': 'UNATHORIZED', 'message': 'invalid key or secret'}, 401
        return {'token': token}, 200

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {'claims': claims}, 200

api_auth.add_resource(CreateTokenUserResource, '')
api_auth.add_resource(RefreshTokenResource, '/refresh')
api_auth.add_resource(CreateTokenAdminResource, '/admin')