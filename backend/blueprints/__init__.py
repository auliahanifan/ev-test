from flask import Flask, request, g
import json, logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# Init Flask
app = Flask(__name__)
CORS(app)

# Set Database
TESTING = bool(os.environ.get('TESTING', False))

if TESTING:
    DB_USERNAME = os.environ.get('DB_TEST_USERNAME', '')
    DB_PASSWORD = os.environ.get('DB_TEST_PASSWORD', '')
    DB_HOST = os.environ.get('DB_TEST_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_TEST_PORT', 3306)
    DB_NAME = os.environ.get('DB_TEST_NAME', '')
else:
    DB_USERNAME = os.environ.get('DB_USERNAME', '')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', 3306)
    DB_NAME = os.environ.get('DB_NAME', '')

app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# JWT
JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', '364'))
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'Ecommerce')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=365)

jwt = JWTManager(app)

# only super admin
def superAdminRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['admin_id'] is not None:
            if not claims['admin_status']: # If berjalan jika statement True, jadi 'not False' = True
                return {'status': 'FORBIDDEN', 'message': 'Internal Only'}, 403
            else:
                return fn(*args, **kwargs)
    return wrapper

# all admin (super and not super)
def adminRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['admin_id'] is not None:
            return fn(*args, **kwargs)
    return wrapper

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

# Middlewares
@app.after_request 
def after_request(response):
    try:        
        if request.method == 'GET':  
            app.logger.warning("REQUEST_LOG\t%s", 
                json.dumps({
                    'method':request.method,
                    'code':response.status,
                    'uri':request.full_path,
                    'request':request.args.to_dict(), 
                    'response':json.loads(response.data.decode('utf-8'))
                    })
            )
        else:
            app.logger.warning("REQUEST_LOG\t%s", 
                json.dumps({
                    'uri':request.full_path,
                    'request':request.get_json(), 
                    'response':json.loads(response.data.decode('utf-8'))
                    })
            )
    except Exception as e:
        app.logger.error("REQUEST_LOG\t%s",
            json.dumps({
                'uri':request.full_path,
                'request':{}, 
                'response':json.loads(response.data.decode('utf-8'))
                })
        )
    
    return response

# Import blueprints
from blueprints.user.resources import bp_user
from blueprints.product.resources import bp_product
from blueprints.auth import bp_auth
from blueprints.user_detail.resources import bp_user_details
from blueprints.transaction.resources import bp_transaction
from blueprints.cart.resources import bp_cart
from blueprints.admin.resources import bp_admin
from blueprints.category.resources import bp_category
from blueprints.transaction_detail.resources import bp_transaction_detail

app.register_blueprint(bp_user, url_prefix = '/api/register')
app.register_blueprint(bp_product, url_prefix = '/api/product')
app.register_blueprint(bp_auth, url_prefix = '/api/login')
app.register_blueprint(bp_user_details, url_prefix = '/api/user_details')
app.register_blueprint(bp_transaction, url_prefix = '/api/transaction')
app.register_blueprint(bp_cart, url_prefix = '/api/cart')
app.register_blueprint(bp_admin, url_prefix = '/api/admin')
app.register_blueprint(bp_category, url_prefix = '/api/category')
app.register_blueprint(bp_transaction_detail, url_prefix = '/api/transaction_details')

db.create_all()
