
from asyncio import tasks
import json
import asyncio
from threading import Thread
from statistics import quantiles
import symbol

# from core.client import AsyncClient, get_ws
# from core.trade import Trade
from core.spot import SpotMarket
from binance.websocket.spot.websocket_client import SpotWebsocketClient
import time

from exchange.binance.client import Client as ExchangeClient

import os
from dotenv import load_dotenv
from runner import init_runner, every

load_dotenv() # take environment from .env

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
testnet = os.getenv('TEST_NET') # use test endpoints


async def main():

    import exchange.binance.websocket

    runner_loop = asyncio.new_event_loop()

    await init_runner(runner_loop)

    return
    
    ###### Testing get trades

    # Base symbol
    symbol = "BTCUSDT"

    client = ExchangeClient(key=api_key, secret=api_secret, testnet=testnet)

    spot_market = SpotMarket(client=client)

    """
    - Money on wallet: 30
    - Amount of transactions: divides the money on wallet in equatitative portions.
    """

    quote_amount = 32 # usd
    # Amount of transactions
    transaction_amount = 1

    portion_price = quote_amount / transaction_amount

    earn_margin = 0.02

    buy_price = 19251.24
    # TODO FIX - When selling. Its rounding up the QTY (amount may not exists)
    quantity = 0.00165

    order = spot_market.make_safe_order(
        symbol=symbol,
        side="SELL",
        earn_margin=earn_margin,
        quote_amount=quote_amount,
        fraction=transaction_amount,
        price=buy_price,
        quantity=quantity,
        # transact_now=True
    )

    print("ORDER")
    if order:
        print(json.dumps(order, indent=2))
  
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



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.run(main())
    loop.run_forever()
    # worker_loop = asyncio.new_event_loop()
    # worker = Thread(target=init_runner, args=(worker_loop, ), daemon=True, name="Runner")
    # worker.start()

   # worker_loop.call_soon_threadsafe(main)
    
    # async def init():
    #     # worker_loop = asyncio.new_event_loop()
    #     # worker = Thread(target=init_runner, args=(worker_loop,), daemon=True)
    #     # worker.start()

    #     # asyncio.run_coroutine_threadsafe(asyncio.create_task(main()), worker_loop)
    #     asyncio.gather(
    #         asyncio.create_task(main()),
    #         # asyncio.create_task(init_runner())
    #     )

    # asyncio.run(init())
    #########
    # loop = asyncio.get_event_loop()
    # loop.call_soon_threadsafe(loop.create_task(main()))

    # try:
    #     loop.run_forever()
    # except asyncio.CancelledError:
    #     loop.close()

"""
******** SPOT *********
exchage-core    | Market Price: 20024.01000000
exchage-core    | Quantity: 0.001548141456181853684651575783
exchage-core    | Performance Fiat: 20064.05802000000000083366689
exchage-core    | Performance %: 4017628.984330602000166933541
exchage-core    | Spread: 40.04802000000000083366689
exchage-core    | ******** END SPOT *********
exchage-core    | 0.001548141456181853684651575783
exchage-core    | 0.00001000
exchage-core    | 9000.00000000
exchage-core    | 20064.05802000000000083366689
exchage-core    | 0.01000000
exchage-core    | 1000000.00000000
exchage-core    | 
exchage-core    |  PLACE LIMIT ORDER BUY 
exchage-core    |  
exchage-core    | Symbol: BTCUSDT
exchage-core    | Qty: 0.00154000
exchage-core    | Price: 20064.05000000
exchage-core    | creating order
exchage-core    | {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC', 'quantity': Decimal('0.00154000'), 'price': Decimal('20064.05000000')}
exchage-core    | ORDER HOOK
exchage-core    | 0rder: {'symbol': 'BTCUSDT', 'orderId': 13575152823, 'orderListId': -1, 'clientOrderId': 'mmxt1FtA6aKor5HkiUj2nU', 'transactTime': 1663469245036, 'price': '20064.05000000', 'origQty': '0.00154000', 'executedQty': '0.00154000', 'cummulativeQuoteQty': '30.83699080', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'fills': [{'price': '20024.02000000', 'qty': '0.00154000', 'commission': '0.00000000', 'commissionAsset': 'BNB', 'tradeId': 1833537025}]}
exchage-core    | ORDER
exchage-core    | {
exchage-core    |   "symbol": "BTCUSDT",
exchage-core    |   "orderId": 13575152823,
exchage-core    |   "orderListId": -1,
exchage-core    |   "clientOrderId": "mmxt1FtA6aKor5HkiUj2nU",
exchage-core    |   "transactTime": 1663469245036,
exchage-core    |   "price": "20064.05000000",
exchage-core    |   "origQty": "0.00154000",
exchage-core    |   "executedQty": "0.00154000",
exchage-core    |   "cummulativeQuoteQty": "30.83699080",
exchage-core    |   "status": "FILLED",
exchage-core    |   "timeInForce": "GTC",
exchage-core    |   "type": "LIMIT",
exchage-core    |   "side": "BUY",
exchage-core    |   "fills": [
exchage-core    |     {
exchage-core    |       "price": "20024.02000000",
exchage-core    |       "qty": "0.00154000",
exchage-core    |       "commission": "0.00000000",
exchage-core    |       "commissionAsset": "BNB",
exchage-core    |       "tradeId": 1833537025
exchage-core    |     }
exchage-core    |   ]
exchage-core    | }



"""