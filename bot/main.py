
from asyncio import tasks
import json
import asyncio
from tkinter.messagebox import RETRY

# from core.client import AsyncClient, get_ws
# from core.trade import Trade
from core.spot import SpotMarket
from binance.websocket.spot.websocket_client import SpotWebsocketClient
import time

from exchange.binance.client import Client as ExchangeClient
import os
from dotenv import load_dotenv
load_dotenv() # take environment from .env
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
testnet = os.getenv('TEST_NET') # use test endpoints


# def start_trading_events(client):
#     print("ASDASD")

#     def message_handler(message):
#         print(message)
    
#     response = client.new_listen_key()


#     print(response)

#     ws_client = SpotWebsocketClient(stream_url="wss://stream.binance.com:9443")
#     ws_client.start()

#     ws_client.user_data(
#         listen_key=response["listenKey"],
#         id=1,
#         callback=message_handler,
#     )

#     time.sleep(30)

#     print("closing ws connection")
#     ws_client.stop()



# scalping stratergy
async def main():
    
    client = ExchangeClient(key=api_key, secret=api_secret, testnet=False)

    # start_trading_events(client)

    
    # bid/ask price and qty
    # r = client.book_ticker('BTCUSDT')
    
    # trade price
    # r = client.ticker_price('BTCUSDT')

    r = client.my_trades('BTCUSDT')

    print(json.dumps(r, indent=2))
    # start_trading_events(client)
    return 




    symbol = 'BTCUSDT'


    tasks = []

    # tasks.append(
    #     start_trading_events(client)
    # )

    ################# Sport market

    spot_market = SpotMarket(client)

    tasks.append(
        spot_market.make_order(symbol)
    )

    await asyncio.gather(*tasks)

    # trade = Trade()
    
    # def socket_callback(r):
    #     print(r)

    # print("**** starting trading ****")
    # await trade.trade_socket(symbol, socket_callback)

    # await client.close_connection()



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())