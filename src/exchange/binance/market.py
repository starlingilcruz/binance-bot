
from decimal import Decimal
from core.enums import  OrderType

def create_market_order(
    client,
    symbol, 
    target_quantity, 
    side, 
    rules = None
):
    pass

def create_order_limit(client, symbol, price, quantity, side):
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'LIMIT', # OrderType.LIMIT,
        'timeInForce': 'GTC',
        'quantity': quantity,
        'price': price
    }

    print("creating order")
    print(params)

    return client.new_order(**params)

def get_all_orders(client, symbol, **kwargs):
    # active, cancel, filled
    return client.get_orders(symbol, **kwargs)

def get_open_orders(client, symbol, **kwargs):
    return client.get_open_order(symbol, **kwargs)

def cancel_order(client, symbol, **kwargs):
    return client.cancel_order(symbol, **kwargs)

def cancel_open_orders(client, symbol, **kwargs):
    return client.cancel_open_orders(symbol, **kwargs)

# TODO move to separated file
# TODO research order rate limi: should not the gt than 60000.
def get_trades(client, symbol, **kwargs):
    return client.my_trades(symbol, **kwargs)

def get_avg_price(client, symbol):
    return Decimal(client.avg_price(symbol).get('price', 0))

def get_ticker_price(client, symbol):
    # print(self.ticker_price(symbol))
    return Decimal(client.ticker_price(symbol).get('price', 0))
        

