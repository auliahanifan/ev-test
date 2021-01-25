from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
import json
from .model import Cart
from ..product.model import Product
from ..user.model import User
from ..cart.model import Cart
from ..transaction_detail.model import TransactionDetails
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app
import datetime 

bp_cart = Blueprint('cart', __name__)
api_cart = Api(bp_cart)


class CartResource(Resource):
   
    def options(self, cart_id=None):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def put(self, cart_id):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        parser.add_argument('qty', location='json', default=1)
        data = parser.parse_args()

        # get user id and query
        claims = get_jwt_claims()
        user_id = claims['user_id']
        qry = Cart.query.get(cart_id)
        # get the product price from product table
        product_price = Product.query.get(int(data['product_id'])).product_price * int(data['qty'])

        #get the product name from product table
        product_name = Product.query.get(int(data['product_id'])).product_name
        
        #check the quantity (apakah masih cukup quantity cart dengan barang)
        product_stock = Product.query.get(int(data['product_id'])).product_stock

        if product_name is not None:
            if product_stock > int(data['qty']):
                qry.qty = data['qty']
                qry.product_id = data['product_id']
                qry.product_name = product_name
                qry.price = product_price
                qry.updated_at = datetime.datetime.now()
                db.session.commit()
                
                return marshal(qry, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'STOCK_NOT_ENOUGH'}, 200, {'Content-Type': 'application/json'}

    # method to add items to cart
    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        parser.add_argument('qty', location='json', default=1)
        data = parser.parse_args()

        # get the product price from product table
        product_price = Product.query.get(int(data['product_id'])).product_price * int(data['qty'])

        #get the product name from product table
        product_name = Product.query.get(int(data['product_id'])).product_name
        
        #check the quantity (apakah masih cukup quantity cart dengan barang)
        product_stock = Product.query.get(int(data['product_id'])).product_stock

        claims = get_jwt_claims()
        user_id = claims['user_id']
        qry = Cart.query.filter_by(user_id = int(user_id)).all()
        cart_items = []

        # Check the previous cart with the cart that will be add, if same, just add the qty
        for item in qry:
            if item.product_id == int(data['product_id']):
                # Check the stock before add the qty
                if product_stock < (item.qty + int(data['qty'])):
                    return {'status': 'Product ID: '+ str(item.product_id) +' Stock Not Enough'}, 400, {'Content-Type': 'application/json'}
                item.qty += int(data['qty'])
                item.price += product_price
                item.updated_at = datetime.datetime.now()
                db.session.commit()    
                return {
                    'status': 'product_id '+ str(item.product_id) + ' has been added ' + str(data['qty'] + ' qty(s)') ,
                    'price' : str(item.price),
                    'qty': str(item.qty),
                    'cart_id': str(item.cart_id)
                    }, 200


        if product_stock < int(data['qty']):
            return {'status': 'Stock Not Enough'}, 400, {'Content-Type': 'application/json'}
        else:

        # adding product to carts
            cart = Cart(
                user_id, 
                data['product_id'], 
                product_name,
                data['qty'],
                product_price
            )

            db.session.add(cart)
            db.session.commit()

            return marshal(cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}
    
    # method to show items inside cart
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = claims['user_id']
        qry = Cart.query.filter_by(user_id = int(user_id)).all()

        cart_items = []
        for item in qry:
            cart_items.append(marshal(item, Cart.response_fields))
        return cart_items, 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, cart_id):
        # to get cart that matches the cart_id
        qry = Cart.query.get(cart_id)
        claims = get_jwt_claims()

        if qry is None:
            return {'status':'CART_NOT_FOUND'}, 400, {'Content-Type': 'application/json'}
        
        # to check if the product is this user's
        if qry.user_id != int(claims['user_id']):
            return {'status':'INVALID_ACTION'}, 400, {'Content-Type': 'application/json'}
        
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'deleted'}, 200, {'Content-Type': 'application/json'}
    
api_cart.add_resource(CartResource, '', '/<cart_id>')


        
