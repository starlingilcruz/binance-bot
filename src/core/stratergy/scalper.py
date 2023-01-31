from core.enums import EventType
from core.events import EventEmitter
from core.misc import reserved_names
from core.trade import TradeType
from .interface import Stratergy

global_config = {
    #'max_chunk_size': 10, # amount is divided by this number
    'fraction': 10, # amount is divided by this number
    'earn_margin': 0.02,

    'logger': lambda x: print(
            """ System Log: {0} """.format(x)
        )
}


def get_config(instance, collection, event):
    # This should mix all global configuration.
    # The idea is to make pre-configured process than can be dinamically applied.
    # Configurations can be created and customized dinamically.

    return {
        'non_filled_orders': collection.non_filled,
        'scalp_filter': lambda x: instance.scalp_filter(x),
        'prepare_place_order': lambda x: event.emit(
            EventType.PREPARE_PLACE_ORDER.value, 
            instance=instance, 
            collection=collection, 
            orders=x,
            **global_config
        ),  

        # No overridable configuration
        **global_config,
    }


class Scalper(Stratergy):
    """ # Attempts to make a profit out of small price movements within exchange market """

    # 1. Process a single currency pair per instance
    # 2.

    trade_type = TradeType.Scalping

    def __init__(self, symbol, client, collection):
        super().__init__(symbol, client, collection)

        self.config = get_config(
            instance=self, collection=collection, event=self.event
        )

    def scalp_filter(self, transactions):
        """ 
            Receives list of transactions/orders to determinated base on 
            conditions, if next transaction can be executed.
        """ 
        
        return transactions

    def monitor(self):
        """ Return dict with properties """
        pass

    def execute_action(self):
        # Attempts to make small profitable movements within the market

        # Scalping should prioritize making hight volumes off small profit.
        # We find from the wallet the assset availability, then split the amount in chuncks
        # that will represents the expected amount of trades.

        # TODO revisit
        # Scalper can be customizable by allocating memory points in an object definition
        # See required object definition (proc, after, unitl, etc.)

        # default action definition

        # 1. find series of buy/sell transaction
        # 2. pass transactions to scalp filter - this identifies if the next transaction
        # can be executed 
        # 3. depending on earn marging defined - execute counterpart trade operation

        default_operation = {
            'fetch': self.config.get('non_filled_orders', lambda x: x),
            'filter': self.config.get('scalp_filter', lambda x: x),
            'submit': self.config.get('prepare_place_order', lambda x: x),
            # 'logger': self.config.get('logger', lambda x: x)
        }
        
        operations = [
            default_operation,
        ]

        for operation in operations:
            procs = operation.keys()
            last_result = None
            for proc_key in procs:
                if proc_key in reserved_names:
                    # TODO move to exceptions.py
                    raise Exception("Use of reserved variable or attribute name")
                last_result = operation.get(proc_key)(last_result)


    def sync_from_exchange(self):
        # TODO fetch for every symbol selected which is stored in the database

        # Look for opens orders in place
        orders = self.client.get_open_orders(self.symbol)

        if orders:
            print("""
                ** Order found in exchange ** \n
                1. Upserting orders for processing \n\n
            """)
            return self.collection.upsert_batch(orders=orders)

        print(""" 
                ** No orders where found in exchange ** \n
                1. Marking processing ones as completed \n\n
            """)
        self.collection.mark_processing_as_completed()
