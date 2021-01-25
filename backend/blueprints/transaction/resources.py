from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
import json
from .model import Transaction
from ..product.model import Product
from ..user.model import User
from ..cart.model import Cart
from ..transaction_detail.model import TransactionDetails
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app, adminRequired
import datetime
import time

bp_transaction = Blueprint('transaction', __name__)
api_transaction = Api(bp_transaction)


class TransactionResource(Resource):

    def options(self, transaction_id=None):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    # transaction method
    @jwt_required
    def post(self):       
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='json', required=True)
        parser.add_argument('handphone', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('city', location='json', required=True)
        parser.add_argument('district', location='json', required=True)
        parser.add_argument('zip_code', location='json', required=True)
        parser.add_argument('note', location='json', required=True)
        data = parser.parse_args() 

        claims = get_jwt_claims()
        user_id = claims['user_id']

        db.session.begin(subtransactions=True)

        cart_qry = Cart.query.filter_by(user_id = int(user_id)).all()
        cart_qry_temp = cart_qry

        products_before = []
        product_after = []

        if cart_qry == []:
            return {'status': 'FAILED', 'note': 'ZERO_CART'}, 400

        # variable for stopping the over-qty cart
        deleted_cart = 0
        total_price = 0

        # iterate to check availability the stock, and also get the total price
        for item in cart_qry:
            product_query = Product.query.filter_by(product_id = item.product_id).first()    
            
            # check the availability of stock 
            if product_query.product_stock < item.qty:
                db.session.delete(item)
                db.session.commit()
                deleted_cart +=1
            else: 
                total_price += item.price
            
            products_before.append(product_query)
            
        if deleted_cart > 0:
            return {'status': 'Stock Not Enough'}, 400, {'Content-Type': 'application/json'}        

        # make a row in transaction table
        transaction = Transaction(user_id, total_price, data['full_name'], data['handphone'],  data['address'], data['province'], data['city'], data['district'], data['zip_code'], data['note'], 0)
        db.session.add(transaction)
        db.session.commit()

        transaction_id = transaction.transaction_id
        
        # iterate again to transaction
        for item in cart_qry:
            product_qry = Product.query.filter_by(product_id = item.product_id).first()
            # to decrease the stock of the product
            product_qry.product_stock -= item.qty
            db.session.commit()

            trans_detail = TransactionDetails(transaction_id, item.product_id, item.product_name, item.qty, item.price)
            # adding into trans_detail table
            db.session.add(trans_detail)
            db.session.commit()

            # delete the items in cart database so that when user make more transaction, the old ones will not be included
            db.session.delete(item)
            db.session.commit()
        
        for item in cart_qry_temp:
            product_query = Product.query.filter_by(product_id = item.product_id).first()    
            product_after.append(product_query)
            if product_query.product_stock < 0:
                db.session.rollback()
                return {'status': 'Stock Not Enough'}, 400, {'Content-Type': 'application/json'}
        
        return marshal(transaction, Transaction.response_fields), 200, {'Content-Type': 'application/json'}
        
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = claims['user_id']
        qry = Transaction.query.filter_by(user_id = int(user_id)).all()
        
        trx_list = []
        for item in qry:
            trx_list.append(marshal(item, Transaction.response_fields))
        return trx_list, 200, {'Content-Type': 'application/json'}

    @jwt_required
    @adminRequired
    def put(self, transaction_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', location='json', required=True)
        data = parser.parse_args()

        qry = Transaction.query.get(transaction_id)
        if qry is None:
            return {'status': 'Transaction Details Not Found'}, 400, {'Content-Type': 'application/json'}

        qry.status = data['status']
        qry.updated_at = datetime.datetime.now()
        db.session.commit()

        return marshal(qry, Transaction.response_fields), 200, {'Content-Type': 'application/json'}

class TransactionList(Resource):
    
    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    @adminRequired
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('orderby', location='args', choices=('id'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Transaction.query

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Transaction.transaction_id))
                else:
                    qry = qry.order_by((Transaction.transaction_id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Transaction.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

api_transaction.add_resource(TransactionResource, '', '/<transaction_id>')
api_transaction.add_resource(TransactionList, '/all')