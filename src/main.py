
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
from runner import init_runner

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

    client = ExchangeClient(api_key=api_key, api_secret=api_secret, testnet=False)
    order_collection = OrderCollection()
    scalper = Scalper(
        client=client, 
        collection=order_collection,
        symbol="BTCUSDT"
    )
    
    def every_five_s():

        # TODO listen for order proceed webook instead. request may be limited

        # strategy - attempts to make a profit out of small price movements within exchange market
        # scalper()
        Scalper.run_all()
        print("Instance len *********** {}".format(len(Scalper.get_instances())))

        # from core.database.collections.system import ResourceCollection

        # r = ResourceCollection()

        # for a in list(r.find({})):
        #     print(a)

    # this can be remove once using the exchange order proceesed webhook
    runner_loop = asyncio.new_event_loop()
    await init_runner(runner_loop, every_five_s)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.run(main())
    loop.run_forever()