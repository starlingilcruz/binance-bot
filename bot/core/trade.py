from binance import AsyncClient, BinanceSocketManager

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


class Trade:
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    async def trade_socket(self, symbol, callback):
        client = await AsyncClient.create(self.api_key, self.api_secret)
        bm = BinanceSocketManager(client)
        # start any sockets here, i.e a trade socket
        ts = bm.trade_socket(symbol)
        # then start receiving messages
        async with ts as tscm:
            while True:
                callback(await tscm.recv())

        await client.close_connection()