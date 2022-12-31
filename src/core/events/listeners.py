# from core.database.collections import OrderCollection
from core.enums import EventType
import copy

from . import EventEmitter

event = EventEmitter()

# order_collection = OrderCollection()

# TODO track global events here

@event.on(EventType.ORDER_FILLED.value)
def on_order_filled(result):
    # TODO store transactions by default?
    pass

@event.on(EventType.ORDER_CANCELLED.value)
def on_order_cancelled(result):
    pass

@event.on(EventType.ORDER_COMPLETED.value)
def on_order_completed(result):
    # no other counterpart order will be placed
    pass

@event.on(EventType.PREPARE_PLACE_ORDER.value)
def on_prepare_place_order(collection, orders):
    print("*** CORE: received prepare place order event")
    # event.emit("TEST", collection)

    orders_copy = list(orders)
    order_count = len(orders_copy)

    # assert order_count > 0, "E - place order: No orders to place"
    if order_count == 0:
        print("*** CORE: E - prepare place order: No orders to place")
        return

    # before placing the order we mark this as processing.
    # processing avoid the order to be loaded and try to duplicate
    # a counterpart order.
    result = collection.mark_batch_as_processing(orders=orders)

    modified_count = sum([r.modified_count for r in result])

    assert modified_count == order_count or modified_count == 0, \
        "Modified count does not match"

    print("*** Marked orders as proccessing ***")

    if modified_count == 0:
        # TODO move this process to corresponding loop
        event.emit(EventType.PLACE_ORDER.value, collection, orders_copy)
    # no other counterpart order will be placed

@event.on(EventType.PLACE_ORDER.value)
def on_place_counterpart_order(collection, orders):
    print("*** CORE: received place counterpart order event")
    order_count = len(list(orders))

    # assert order_count > 0, "E - place order: No orders to place"
    if order_count == 0:
        print("*** CORE: E - place order: No orders to place")
        return

    print("*** Core: Evited - placing counterpart order ***")

    # no other counterpart order will be placed
