# Online Store API

## Background of PoC
Users were able to purchase items (put items in cart, check out, pay) but _actually_ the stocks is not enough. So, Costumer Service cancelled the order due to stock unavailability.
### Troubleshooting
#### Why It Can Be Happened
Due to high traffic, query and command in ORM/SQL become _not normal_, so if the system has checked the stock by query and then... when update, the stock can be different. That's why the data become inconsistent.
#### Solution To Be Proposed
Making system **double check** of the stock, before _update_ to check the availability of stock, and after _update_ to check is the stock under zero or not, if yes (the stock become under zero after update), just rollback the transaction.

# PoC

This is PoC of ecommerce.

___

## Requirements

1. Python 3.7+
2. MySQL

___

## Operations

### Configs

All configs is stored in `.env` file, please create your own `.env` file, the example is in `.env-sample` file.

Note:
There is 2 database: for production and testing. Please fill it.
If environment variable `TESTING=True`, database used is for testing.

### Testing
You can test this code:
1. Activate VirtualEnv first.
2. `pip install -r requirements.txt`
3. Set environment variable `TESTING=True` (you can use .env)
4. Make sure you have migrate, `python app.py db migrate`
5. Make sure your db is filled, you can seed it by `python app.py seed`
6. `pytest --cov-report html --cov=blueprints tests`

### Run
You can run this app by:
1. Activate VirtualEnv.
2. `pip install -r requirements.txt`
3. Make sure all `.env` have been filled truly, also `TESTING=` for running
4. Make sure you have migrate, `python app.py db migrate`
5. `python app.py`