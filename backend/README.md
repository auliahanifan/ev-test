# Online Store API

## Background of PoC
Users were able to purchase items (put items in cart, check out, pay) but _actually_ the stocks is not enough. So, Costumer Service cancelled the order due to stock unavailability.
### Troubleshooting
#### Why It Can Be Happened
The system DIDN'T CHECK stock before PURCHASE. So, there is **difference stocks** between when they put items in stock and purchased it. 
#### Solution To Be Proposed
Making system check the stock again while purchasing. And make the handler in stock so it cannot be zero stock.
