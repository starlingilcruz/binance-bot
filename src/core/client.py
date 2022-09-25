# import os

# from binance import AsyncClient as BaseAsyncClient
# from dotenv import load_dotenv

# load_dotenv() # take environment from .env

# api_key = os.getenv('API_KEY')
# api_secret = os.getenv('API_SECRET')
# testnet = os.getenv('TEST_NET') # use test endpoints

class Hook:

    def on_order_created(self, **kwargs):
        pass


class Client(Hook):

    def create_order_market_sell(
        self, 
        symbol, 
        target_quantity, 
        rules = None,
        **kwargs
    ):
        pass

    def create_order_limit(
        self,
        symbol, 
        target_price, 
        target_quantity, 
        side, # BUY / SELL
        rules = None,
        **kwargs
    ):
        pass

    def create_stop_limit_order(self):
        pass

