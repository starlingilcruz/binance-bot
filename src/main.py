
# from asyncio import tasks
# import json
import asyncio
# from threading import Thread
# from statistics import quantiles
# import symbol

from core.spot import SpotMarket
from core.database.collections import OrderCollection
from core.stratergy.scalper import Scalper

# from binance.websocket.spot.websocket_client import SpotWebsocketClient
# import time

from exchange.binance.client import Client as ExchangeClient

import os
from dotenv import load_dotenv
from runner import init_runner, every

load_dotenv() # take environment from .env

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
testnet = os.getenv('TEST_NET') # use test endpoints


"""
    - get legal coin information and research for symbols
    - create symbol list
        - from exchange
        - from user wallet: (v1)
            user wallet symbols are possible symbols that can be used to make an order.
    - pick symbol from list to create order (buy/sell):
        - get price in market
        - should determinate perfect price and quantity
        - wait for order to be filled
        - go to next step and then repeat this process
    - store order filled information, performance %, earn, repr in USD.    
    """


async def main():

    """
        1. have runner to be responsible of processes in different timming.
        2. call function to see if there are open orders
        3. if no open orders. call function to create order.
        4. to determinate the side of the order. must store the last transaction.
        5. before create the order, check last transaction to create the propper variables
        6. tbd.
    """

    symbol = "BTCUSDT"

    client = ExchangeClient(key=api_key, secret=api_secret, testnet=False)

    order_collection = OrderCollection()
    
    scalper = Scalper(client=client, collection=order_collection)
    
    def every_five_s():

        """
            TODO listen for order proceed webook instead. 
            request may be limited
        """
        print("5 SEC")

        # Stratergies will be iteratin by the runner, and the configuration is loaded per individual class instance
        scalper()

        # Find open orders
        orders = client.get_open_orders(symbol)

        if not orders:
            print("NO ORDERS FOUND")

            order_collection.mark_processing_as_completed()
            # the order is not filled yet, so we store it as filled false.
            # by default a new order should always created with filled false value.

            # find all filled false orders and mark as filled
            # TODO when cancelling an order through the exchange is not being determitated here

            # TODO implement query cache in underlying function
            return 


        # if orders are found in place, then we store it.
        order_collection.insert_many(documents=orders, id_key='orderId')

    runner_loop = asyncio.new_event_loop()
    await init_runner(runner_loop, every_five_s)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.run(main())
    loop.run_forever()