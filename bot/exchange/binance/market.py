from decimal import Decimal
from core.enums import  OrderType


def create_market_order(
    self,
    symbol, 
    target_quantity, 
    side, 
    rules = None
):
    pass

def create_order_limit(self, symbol, price, quantity, side):
    params = {
        'symbol': symbol,
        'side': side,
        'type': OrderType.LIMIT,
        'timeInForce': 'GTC',
        'quantity': quantity,
        'price': price
    }

    return self.new_order(**params)

def get_avg_price(self, symbol):
    return Decimal(self.avg_price(symbol).get('price', 0))
        