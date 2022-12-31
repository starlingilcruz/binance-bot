# scalper.py is a tentative name.
# TODO maybe consider a better name

from core.enums import EventType
# import asyncio
# import inspect
# from types import coroutine
from core.events import EventEmitter
from core.misc import reserved_names



def get_config(instance, collection, event):
    # This should mix all global configuration.
    # The idea is to make pre-configured process than can be dinamically applied.
    # Configurations can be created and customized dinamically.

    return {
        'non_filled_orders': collection.non_filled,
        'prepare_place_order': lambda x: event.emit(
            EventType.PREPARE_PLACE_ORDER.value, collection, x
        ),
    }


class Scalper():
    # TODO find better class name that defines the process specs.
    # 1. The propurse of this processor is to find orders that remains opens and make
    # an opposite orders for it.
    # 2. Orders have an unique id and each transaction should specify a parent order reference id.
    # 3. This runs forevere. TODO revisit.

    def __init__(self, client, collection):
        print("SCALPER INSTANCE")
        self.client = client
        self.collection = collection
        self.event = EventEmitter()

        self.config = get_config(
            instance=self, collection=collection, event=self.event
        )

        # Block proccess to avoid query for non filled orders while 
        # other procedures are still running. Once all procedures
        # completes, unblock the proccess.
        self._block_current_proccess = False

    def __call__(self):
        print("*** Scalper Processing ***")

        # Track listener result and pass it to next iteration
        # last_result = None
        
        # runs a series of tasks secuentially and repeatly

        # 1. fetch orders with processed = false
        # order processed means that an opossite order are in place

        # 2. place an opossite order with earn margin 
        # here we can calculate an effective earn margin and split into micro orders

        # TODO revisit
        # Scalper can be customizable by allocating memory points in an object definition
        # See required object definition (proc, after, unitl, etc.)
        listeners = [
            {
                'a': self.config.get('non_filled_orders', lambda x: x),
                # 'b': self.config.get('mark_orders_as_processing', lambda x: x),
                'c': self.config.get('prepare_place_order', lambda x: x),
                # 'each': 4 # complete, forever or time in miliseconds
            },
            # This could be N amount of listeners
        ]

        for listener in listeners:
            procs = listener.keys()
            last_result = None
            for proc_key in procs:
                if proc_key in reserved_names:
                    # TODO move to exceptions.py
                    raise Exception("Use of reserved variable or attribute name")
                last_result = listener.get(proc_key)(last_result)

