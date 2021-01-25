import pytest, json, logging
from flask import Flask, request, json
from blueprints import app
from app import cache

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token_admin_non_super():
    token = cache.get('token-non-super')
    if token is None:
        ## prepare request input
        data = {
            "username": "adminbiasa",
            "password": "adminbiasa"
        }

        ## do request
        req = call_client(request)
        res = req.post('/api/login/admin',
                        data=json.dumps(data),
                        content_type='application/json') # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-non-internal', res_json['token'], timeout=60)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token


def create_token_admin_super():
    token = cache.get('token-super')
    if token is None:
        ## prepare request input
        data = {
            "username": "admin",
            "password": "admin"
        }

        ## do request
        req = call_client(request)
        res = req.post('/api/login/admin',
                        data=json.dumps(data),
                        content_type='application/json') # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-internal', res_json['token'], timeout=60)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token
    
def create_token_user_first():
    token = cache.get('token-user1')
    if token is None:
        ## prepare request input
        data = {
            "username": "user",
            "password": "user"
        }

        ## do request
        req = call_client(request)
        res = req.post('/api/login',
                        data=json.dumps(data),
                        content_type='application/json') # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-user1', res_json['token'], timeout=100)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token

def create_token_user_second():
    token = cache.get('token-user2')
    if token is None:
        ## prepare request input
        data = {
            "username": "userbaru",
            "password": "userbaru"
        }

        ## do request
        req = call_client(request)
        res = req.post('/api/login',
                        data=json.dumps(data),
                        content_type='application/json') # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-user2', res_json['token'], timeout=100)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token
