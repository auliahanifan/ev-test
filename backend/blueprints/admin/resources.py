from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Admin
from sqlalchemy import desc
from blueprints import app, db, superAdminRequired
from flask_jwt_extended import jwt_required
import datetime

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

class AdminResource(Resource):
    
    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    # @jwt_required
    # @superAdminRequired
    def get(self, id): # get by id
        qry = Admin.query.get(id)
        if qry is not None:
            return marshal(qry, Admin.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'User Not Found'}, 400, {'Content-Type': 'application/json'}

    # @jwt_required
    # @superAdminRequired
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        parser.add_argument('status', type=bool, location='json')
        data = parser.parse_args()

        user = Admin(data['username'], data['password'], data['status'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Admin.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    # @superAdminRequired
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        parser.add_argument('status', type=bool, location='json', required=True)
        args = parser.parse_args()

        qry = Admin.query.get(id)
        if qry is None:
            return {'status': 'User Not Found'}, 400, {'Content-Type': 'application/json'}

        qry.admin_username = args['username']
        qry.admin_password = args['password']
        qry.admin_status = args['status']
        qry.updated_at = datetime.datetime.now()
        db.session.commit()

        return marshal(qry, Admin.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    # @superAdminRequired
    def delete(self, id):
        qry = Admin.query.get(id)
        if qry is None:
            return {'status': 'User Not Found'}, 400, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'User Deleted'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501


class AdminList(Resource):

    def __init__(self):
        pass

    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}

    # @jwt_required
    # @superAdminRequired
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('status', type=inputs.boolean, location='args', choices=(True, False))
        parser.add_argument('orderby', location='args', choices=('id', 'status'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Admin.query

        if args['status'] is not None:
            qry = qry.filter_by(status=args['status'])

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Admin.id)) # bisa gini
                else:
                    qry = qry.order_by((Admin.id))
            elif args['orderby'] == 'status':
                if args['sort'] == 'desc':
                    qry = qry.order_by((Admin.id).desc()) # bisa juga gini   
                else:
                    qry = qry.order_by((Admin.id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Admin.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}


api.add_resource(AdminList, '')
api.add_resource(AdminResource, '', '/<id>')