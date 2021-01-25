from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
import json
from .model import TransactionDetails
from ..transaction.model import Transaction
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app

bp_transaction_detail = Blueprint('transaction_detail', __name__)
api = Api(bp_transaction_detail)

class TransactionDetailsList(Resource):

    def options(self):
        return {'status': 'success'}, 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = claims['user_id']
        trx_qry = Transaction.query.filter_by(user_id = int(user_id)).all()

        trx_ids = []
        for item in trx_qry:
            trx_ids.append(item.transaction_id)

        trx_details = []
        for trx_id in trx_ids:
            trx_detail_qry = TransactionDetails.query.filter_by(transaction_id = int(trx_id)).all()
            for trx in trx_detail_qry:
                trx_details.append(marshal(trx, TransactionDetails.response_fields))

        return trx_details, 200, {'Content-Type': 'application/json'}

class TransactionDetailsResource(Resource):

    def options(self, transaction_id = None):
        return {'status': 'success'}, 200
    

    @jwt_required
    def get(self, transaction_id):
        # for authenticaton only
        claims = get_jwt_claims()
        user_id = claims['user_id']
        trx_qry = Transaction.query.get(transaction_id)
        if int(user_id) != int(trx_qry.user_id):
            return {'status': 'NOT_ALLOWED'}, 401, {'Content-Type':'application/json'}
      
        # getting the details
        trx_details = []
        trx_detail_qry = TransactionDetails.query.filter_by(transaction_id = transaction_id).all()
        for trx in trx_detail_qry:
            trx_details.append(marshal(trx, TransactionDetails.response_fields))

        return trx_details, 200, {'Content-Type': 'application/json'}

api.add_resource(TransactionDetailsList, '')
api.add_resource(TransactionDetailsResource, '', '/<transaction_id>')