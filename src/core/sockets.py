from binance import BinanceSocketManager

from .client import AsyncClient

"""
  Binance API documentation

  response = {
      "e": "aggTrade",  // Event type
      "E": 123456789,   // Event time
      "s": "BNBBTC",    // Symbol
      "a": 12345,       // Aggregate trade ID
      "p": "0.001",     // Price
      "q": "100",       // Quantity
      "f": 100,         // First trade ID
      "l": 105,         // Last trade ID
      "T": 123456785,   // Trade time
      "m": true,        // Is the buyer the market maker?
      "M": true         // Ignore
    }
"""
# binance order filters
# https://sammchardy.github.io/binance-order-filters/

class Socket:
    
    def __init__(self, **kwargs):
        self.testnet = kwargs.get('testnet')

    async def trade_socket(self, symbol, callback):
        client = await AsyncClient.create(testnet=self.testnet)
        bm = BinanceSocketManager(client)
        # start any sockets here, i.e a trade socket
        ts = bm.trade_socket(symbol)
        # then start receiving messages
        async with ts as tscm:
            while True:
                callback(await tscm.recv())

        await client.close_connection()