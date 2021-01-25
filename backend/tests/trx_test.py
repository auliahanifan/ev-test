import json
from . import app, client, cache, create_token_user_first, create_token_user_second
class TestClientCrud():
    
    # post Cart
    def test_cart_input(self, client):
        token = create_token_user_first()
        data = {
            "product_id": 1,
            "qty": 99
        }
        res=client.post('/api/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        print(res_json)
        TestClientCrud.var_id = res_json['cart_id']

        assert res.status_code == 200

    def test_cart_input_2(self, client):
        token = create_token_user_second()
        data = {
            "product_id": 1,
            "qty": 99
        }
        res=client.post('/api/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        print(res_json)
        TestClientCrud.var_id = res_json['cart_id']

        assert res.status_code == 200

    def test_transaction_input(self, client):
        token = create_token_user_first()
        data = {
            "full_name": "katrok",
            "handphone": "085726262626",
            "address": "jln. a no.2",
            "province": "jawa tengah",
            "city": "purwokerto",
            "district": "pwt timurr",
            "zip_code": "53161",
            "note": ""
        }
        res=client.post('/api/transaction', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        print(res_json)
        TestClientCrud.var_id = res_json['transaction_id']

        assert res.status_code == 200

    def test_transaction_input_2(self, client):
        token = create_token_user_second()
        data = {
            "full_name": "katrok",
            "handphone": "085726262626",
            "address": "jln. a no.2",
            "province": "jawa tengah",
            "city": "purwokerto",
            "district": "pwt timurr",
            "zip_code": "53161",
            "note": ""
        }
        res=client.post('/api/transaction', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        print(res_json)
        TestClientCrud.var_id = res_json['transaction_id']

        assert res.status_code == 200

