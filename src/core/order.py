from .rules import Rule


class Order:

    def __init__(self, client):
        self.client = client

    def create_market_order(
        self, 
        symbol, 
        target_quantity, 
        side, 
        rules = None
    ):
        """ 
            Market order is immediatly matched with the best available 
            market price.
        """

        order_qty = target_quantity

        if rules:
            assert isinstance(rules, Rule), "Rules should be instance of Rule"
  
            # TODO check if value is valid before, to avoid apply the rule
            _, heigher_qty = rules.get_min_max_quantity(target_quantity)

            order_qty = heigher_qty
        
        # print("PLACE MARKET ORDER SELL")
        # print('Symbol: {}'.format(symbol))
        # print('Qty: {}'.format(order_qty))

        order = self.client.create_order_market_sell(
            symbol=symbol, quantity=order_qty
        )
        
        if order:
            self.on_order_created(order)

        return order

    def create_limit_order(
        self, 
        symbol, 
        target_price, 
        target_quantity, 
        side, # BUY / SELL
        rules = None
    ):
        """ 
            Limit order is an order to buy or sell at a specific price or better. 
            Are not guarantee to execute.

            Place order considering any exchange-api rule or limits.
        """
        quantity = target_quantity
        price = target_price

        if rules:
            assert isinstance(rules, Rule), "Rules should be instance of Rule"

            if side == 'SELL':
                # we want to sell at hiegher price posible
                _, quantity = rules.get_min_max_quantity(target_quantity)
                _, price = rules.get_min_max_price(target_price)
            elif side == 'BUY':
                # we want to buy at lower price posible
                quantity, _ = rules.get_min_max_quantity(target_quantity)
                price, _ = rules.get_min_max_price(target_price)
            else:
                # TODO throw exception instead
                raise "Invalid order operation. Param 'side' is invalid."

        # print("\n PLACE LIMIT ORDER {} \n ".format(side))
        # print('Symbol: {}'.format(symbol))
        # print('Qty: {}'.format(quantity))
        # print('Price: {}'.format(price))

        order = self.client.create_order_limit(
            symbol=symbol,
            price=price,
            quantity=quantity,
            side=side
        )
        
        if order:
            self.on_order_created(order)

        return order

    def create_stop_limit_order(self):
        """ To buy or sell a coin once the price reaches a specified amount. """
        pass

    def on_order_created(self, order):
        print('0rder: {}'.format(order))
        
