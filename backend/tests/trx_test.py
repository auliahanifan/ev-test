import json
from . import app, client, cache, create_token_user_first, create_token_user_second, create_token_admin_super
class TestClientCrud():
    
    # post Cart
    # def test_cart_input(self, client):
    #     token = create_token_user_first()
    #     data = {
    #         "product_id": 1,
    #         "qty": 99
    #     }
    #     res=client.post('/api/cart', 
    #                     headers={'Authorization': 'Bearer ' + token},
    #                     data=json.dumps(data),
    #                     content_type='application/json')

    #     res_json=json.loads(res.data)
    #     print(res_json)

    #     assert res.status_code == 200

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

        assert res.status_code == 200

    # def test_transaction_input(self, client):
    #     token = create_token_user_first()
    #     data = {
    #         "full_name": "katrok",
    #         "handphone": "085726262626",
    #         "address": "jln. a no.2",
    #         "province": "jawa tengah",
    #         "city": "purwokerto",
    #         "district": "pwt timurr",
    #         "zip_code": "53161",
    #         "note": ""
    #     }
    #     res=client.post('/api/transaction', 
    #                     headers={'Authorization': 'Bearer ' + token},
    #                     data=json.dumps(data),
    #                     content_type='application/json')

    #     res_json=json.loads(res.data)
    #     print(res_json)
    #     print(res.data)
    #     assert res.status_code == 200

    def test_product_put(self, client):
        token = create_token_admin_super()
        data = {
            "product_name": "Red Tee",
            "product_stock": 100,
            "product_price": 25000,
            "product_weight": 300,
            "product_image_url": "https://images-na.ssl-images-amazon.com/images/I/4166cMJCseL._SR600%2C315_PIWhiteStrip%2CBottomLeft%2C0%2C35_PIStarRatingTWO%2CBottomLeft%2C360%2C-6_SR600%2C315_ZA(23%20Reviews)%2C445%2C291%2C400%2C400%2Carial%2C12%2C4%2C0%2C0%2C5_SCLZZZZZZZ_.jpg",
            "product_description": "Red Tee",
            "category_id": 1
        }
        res=client.put('/api/product/1', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200
