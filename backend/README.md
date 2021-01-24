# Online Store API

## Background of PoC
Users were able to purchase items (put items in cart, check out, pay) but _actually_ the stocks is not enough. So, Costumer Service cancelled the order due to stock unavailability.
### Troubleshooting
#### Why It Can Be Happened
Due to high traffic, query and command in ORM/SQL become _not normal_, so if the system has checked the stock by query and then... when update, the stock can be different. That's why the data become inconsistent.
#### Solution To Be Proposed
Making system **double check** of the stock, before _update_ to check the availability of stock, and after _update_ to check is the stock under zero or not, if yes (the stock become zero after update), just rollback the transaction.
