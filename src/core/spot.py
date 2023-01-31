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

    def make_safe_order(
        self, 
        symbol, 
        side, 
        earn_margin, 
        price = None, 
        quantity = None, 
        **kwargs
    ):
        # Make buy/sell order and guarantee a safe trade.

        # Available amount in the wallet
        quote_amount = kwargs.get("quote_amount", 0)
        assert quote_amount > 0, "Inssuficient quote amount"

        # How many transaction want to make with the available quote_amount
        fraction = kwargs.get("fraction", 1)
        # When true, indicates the transaction have to be executed at current price
        transact_now = kwargs.get("transact_now", False)

        # I.E 30USD / 2
        fraction_quote_amount = quote_amount / fraction

        # Getting price
        if not price:
            price = self.client.get_ticker_price(symbol=symbol)
        else:
            price = Decimal(price)

        # Getting quantity
        # Qty is the portion that represents the quote_amount regarding the price.
        if not quantity:
            quantity = quote_amount / price
        else:
            quantity = Decimal(quantity)
        
        # We perform the transaction applying the earn margin to the current price.
        # When buying the earn margin is (optional).
        # When selling always apply the earn margin.
        if side == "BUY":
            if transact_now:
                # Do the transaction at current price (without earn margin)
                performance_f = price
            else:
                # Apply earn margin
                performance_f = price - (price * Decimal(earn_margin))
        elif side == "SELL":
            # Apply earn margin
            performance_f = price + (price * Decimal(earn_margin))

        print("******** SPOT INFORMATION *********")
        performance_p = earn_margin * 100
        print("Market Price: {}".format(price))
        print("Market Quantity: {}".format(quantity))
        print("Performance Fiat: {}".format(performance_f))
        print("Performance %: {}".format(performance_p))
        print("Spread: {}".format(performance_f - price))
        print("******** END SPOT INFORMATION *********")
        
        print(performance_f)
        # print(price + (price * Decimal(earn_margin)))
       
        info = self.client.exchange_info(symbol).get('symbols')[0]
        
        rules = Rule(symbol_info=info)

        return self.order.create_limit_order(
            symbol=symbol,
            target_price=performance_f,
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