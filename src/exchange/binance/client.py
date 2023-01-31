
from binance.spot import Spot

# https://api1.binance.com
# https://api2.binance.com
# https://api2.binance.com

testnet_url = 'https://testnet.binance.vision'

class Client(Spot):

    from .account import account_balance
    # Market
    from .market import (create_market_order, create_order_limit,
                         get_avg_price, get_ticker_price)
    # Wallet
    from .wallet import coins_info, get_account, get_asset_balance

    def __init__(self, *args, **kwargs):
        if kwargs.pop('testnet', None):
            kwargs.update({
                'base_url': testnet_url
            })
            print("**** Initializing in TEST mode **** \n\n")
        else:
            print("**** Initializing Client **** \n\n")
        print(kwargs)
        super().__init__(*args, **kwargs)