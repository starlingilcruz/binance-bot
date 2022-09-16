import json
from decimal import Decimal

from .order import Order
from .rules import Rule

earn_margin = 0.1

class SpotMarket:
    """ Helper class to find best performance in a transaction """

    def __init__(self, client, order = None):
        self.client = client
        self.order = order

        if not self.order:
            self.order = Order(client)

    @property
    def order(self):
        return self.order

    def make_order(self, symbol, side, earn_margin, quantity):        
        price = self.client.get_avg_price(symbol=symbol)

        # TODO find price correctly and calculate a new price
        # including the earing maring.

        if not price:
          raise "Invalid symbol - price not found"

        # TODO reach any rules required for this transaction
       
        quantity = Decimal(0.001000)

        info = self.client.exchange_info(symbol).get('symbols')[0]

        rules = Rule(symbol_info=info)

        return self.order.create_limit_order(
            symbol=symbol,
            target_price=price,
            target_quantity=quantity,
            side=side,
            rules=rules
        )



"""
    {
        'symbol': 'BTCUSDT', 'orderId': 14712192, 'orderListId': -1, 'clientOrderId': 'iz9qNdeRL9GXWJb9UnjnSO', 
        'transactTime': 1661898591296, 'price': '19790.40000000', 'origQty': '0.00100100', 'executedQty': '0.00000000', 
        'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'fills': []
    }

    {
        'e': 'executionReport', 'E': 1661898606376, 's': 'BTCUSDT', 'c': 'iz9qNdeRL9GXWJb9UnjnSO', 
        'S': 'SELL', 'o': 'LIMIT', 'f': 'GTC', 'q': '0.00100100', 'p': '19790.40000000', 'P': '0.00000000', 
        'F': '0.00000000', 'g': -1, 'C': '', 'x': 'TRADE', 'X': 'FILLED', 'r': 'NONE', 'i': 14712192, 'l': '0.00100100', 
        'z': '0.00100100', 'L': '19790.40000000', 'n': '0.00000000', 'N': 'USDT', 'T': 1661898606376, 
        't': 4441944, 'I': 33846867, 'w': False, 'm': True, 'M': True, 'O': 1661898591296, 'Z': '19.81019040', 
        'Y': '19.81019040', 'Q': '0.00000000'
    }


"""