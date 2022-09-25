from binance.websocket.spot.websocket_client import SpotWebsocketClient
  

def message_handler(message):
    print(message)

ws_client = SpotWebsocketClient()
ws_client.start()

ws_client.book_ticker(
    symbol='btcusdt',
    id=1,
    callback=message_handler,
)
