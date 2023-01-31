
import os
from dotenv import load_dotenv

load_dotenv() # take environment from .env

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

from core.enums import EventType
from core.events import EventEmitter
from core.spot import SpotMarket
from exchange.binance.client import Client as ExchangeClient


def asset_balance_transaction(client, side, symbol):
    if side == "BUY":
        # quote balance
        balance = client.get_asset_balance(symbol[3:])
    elif side == "SELL":
        # asset/coin balance
        balance = client.get_asset_balance(symbol[:3])
    
    if not balance:
        return None

    return balance.get("free")

def transaction_side(current_side):
    return { 'BUY': 'SELL', 'SELL': 'BUY' }[current_side]


def handle_opposite_order(client, collection, data):
    if not data:
        print('no order in collection')
        return 

    if not data.get('filled'):
        print('order:{0} was placed and waiting to be filled'.format(data.get('orderId')))
        return 

    client = ExchangeClient(key=api_key, secret=api_secret, testnet=False)
    spot_market = SpotMarket(client=client)

    operation_id = data.get('id')

    symbol = data.get('symbol')
    active_order_side = data.get('side')
    price = data.get('price')
    origQty = data.get('origQty')

    default_earn_margin = 0.01

    asset_balance = asset_balance_transaction(
        client, transaction_side(active_order_side), symbol
    )

    if active_order_side == 'BUY':
        print(symbol)
        print(transaction_side(active_order_side))
        print(default_earn_margin)
        print(float(price))
        print(1)
        print(price)
        print(origQty)
        print("BUY")

        new_order = spot_market.make_safe_order(
            symbol=symbol,
            side=transaction_side(active_order_side),
            earn_margin=default_earn_margin,
            quote_amount=float(price), # account balance
            fraction=1, # TODO revisit
            price=price, # buy price
            quantity=origQty,
            # transact_now=True
        )

    if active_order_side == 'SELL':
        print(symbol)
        print(transaction_side(active_order_side))
        print(default_earn_margin)
        print(asset_balance)
        print(1)
        print("SELL")
        print(data)
        new_order = spot_market.make_safe_order(
            symbol=symbol,
            side=transaction_side(active_order_side),
            earn_margin=default_earn_margin,
            quote_amount=asset_balance,
            fraction=1, # TODO revisit
            transact_now=True # buy now
        )

    # mark previous order as filled
    collection.mark_as_filled(order_id=data.get('orderId'))

    # insert new created order and assign old one as parent
    new_order.update({ 'parent_id': data.get('orderId') })
    collection.insert_many(documents=[new_order], id_key='orderId')

    print('New Order', new_order)


event = EventEmitter()

@event.on(EventType.PLACE_ORDER.value)
def on_place_counterpart_order(instance, collection, orders, **kwargs):
    print("**** on_place_counterpart_order *****")

    print(orders[0])
    print("\n\n")

    handle_opposite_order(client=None, collection=collection, data=orders[0])