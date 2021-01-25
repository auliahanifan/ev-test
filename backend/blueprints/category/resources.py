from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Category
from sqlalchemy import desc
from blueprints import app, db, adminRequired
from flask_jwt_extended import jwt_required
import datetime

bp_category = Blueprint('category', __name__)
api = Api(bp_category)

class CategoryResource(Resource):

    def __init__(self):
        pass
    
    def options(self, id=None):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
        
    # @jwt_required
    # @internal_required
    def get(self, id): # get by id
        qry = Category.query.get(id)
        if qry is not None:
            return marshal(qry, Category.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'User Not Found'}, 400, {'Content-Type': 'application/json'}

    @jwt_required 
    @adminRequired
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        data = parser.parse_args()

        user = Category(data['name'], data['description'])
        db.session.add(user)
        
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Category.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @adminRequired
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        args = parser.parse_args()

        qry = Category.query.get(id)
        if qry is None:
            return {'status': 'User Not Found'}, 400, {'Content-Type': 'application/json'}

        qry.category_name = args['name']
        qry.category_description = args['description']
        qry.updated_at = datetime.datetime.now()
        db.session.commit()

        return marshal(qry, Category.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @adminRequired
    def delete(self, id):
        qry = Category.query.get(id)
        if qry is None:
            return {'status': 'Category Not Found'}, 400, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'Category Deleted'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501



class CategoryList(Resource):

    def __init__(self):
        pass
    
    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    # @jwt_required
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('orderby', location='args', choices=('id'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Category.query


        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Category.category_id)) # bisa gini
                else:
                    qry = qry.order_by((Category.category_id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Category.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}




api.add_resource(CategoryList, '')
api.add_resource(CategoryResource, '', '/<id>')