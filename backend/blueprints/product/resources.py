from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import Product
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from blueprints import db, app, superAdminRequired, adminRequired
import json
import datetime

bp_product = Blueprint('product', __name__)
api_product = Api(bp_product)

class ProductResource(Resource):
        
    def options(self, product_id=None):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
        
    # method to get product by id
    def get(self, product_id):
        qry = Product.query.get(product_id)
        if qry is not None:
            return marshal(qry, Product.response_fields), 200
        return {'status':'PRODUCT_NOT_FOUND'}, 400

    # method to post new items
    @jwt_required
    @adminRequired
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_name', location = 'json', required = True)
        parser.add_argument('product_stock', location = 'json', required = True)
        parser.add_argument('product_price', location = 'json', required = True)
        parser.add_argument('product_weight', location = 'json', required = True)
        parser.add_argument('product_image_url', location = 'json', required = True)
        parser.add_argument('product_description', location = 'json', required = True)
        parser.add_argument('category_id', location = 'json', required = True)

        # to get data from body
        data = parser.parse_args()
        # to get data from jwt claims
        claims = get_jwt_claims()

        product = Product(int(claims['admin_id']), data['category_id'], data['product_name'], data['product_stock'], data['product_price'], data['product_weight'], data['product_image_url'], data['product_description'])
        db.session.add(product)
        db.session.commit()

        app.logger.debug('DEBUG: %s', product)

        return marshal(product, Product.response_fields), 200, {'Content-Type':'application/json'}

    # method to edit Product
    @jwt_required
    @adminRequired
    def put(self, product_id):
        # to get the product that want to be edited
        qry = Product.query.get(product_id)

        parser = reqparse.RequestParser()
        parser.add_argument('product_name', location = 'json', required = True)
        parser.add_argument('product_stock', location = 'json', required = True)
        parser.add_argument('product_price', location = 'json', required = True)
        parser.add_argument('product_weight', location = 'json', required = True)
        parser.add_argument('product_image_url', location = 'json', required = True)
        parser.add_argument('product_description', location = 'json', required = True)
        parser.add_argument('category_id', location = 'json', required = True)

        data = parser.parse_args()

        if qry is None:
            return {'status':'PRODUCT_NOT_FOUND'}, 400
             
        qry.product_name = data['product_name']
        qry.product_stock = data['product_stock']
        qry.product_price = data['product_price']
        qry.product_weight = data['product_weight']
        qry.product_image_url = data['product_image_url']
        qry.product_description = data['product_description']
        qry.category_id = data['category_id']
        qry.updated_at = datetime.datetime.now()

        db.session.commit()

        return marshal(qry, Product.response_fields), 200
    
    # method to delete product
    @jwt_required
    @adminRequired
    def delete(self, product_id):
        # to get product that matches the product id
        qry = Product.query.get(product_id)
        claims = get_jwt_claims()

        if qry is None:
            return {'status':'PRODUCT_NOT_FOUND'}, 400
        
        db.session.delete(qry)
        db.session.commit()
        return {'status':'PRODUCT_DELETED'}, 200

class ProductList(Resource):

    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('orderby', location='args', choices=('id'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Product.query

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Product.product_id)) 
                else:
                    qry = qry.order_by((Product.product_id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Product.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}


class ProductListByCategory(Resource):

    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    def get(self, category_id):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('orderby', location='args', choices=('id'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Product.query.filter_by(category_id = category_id)

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Product.product_id)) 
                else:
                    qry = qry.order_by((Product.product_id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Product.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

api_product.add_resource(ProductResource, '', '/<product_id>')
api_product.add_resource(ProductList, '/all')
api_product.add_resource(ProductListByCategory, '/category/<category_id>')