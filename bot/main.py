import os
import json
import asyncio
from dotenv import load_dotenv

from binance import AsyncClient, BinanceSocketManager

from core.trade import Trade


load_dotenv() # take environment from .env

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

# scalping stratergy
async def main():

    trade = Trade(api_key, api_secret)

    symbol = 'BNBBTC'
    
    def socket_callback(r):
        print(r)

    print("**** starting trading ****")
    await trade.trade_socket(symbol, socket_callback)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())