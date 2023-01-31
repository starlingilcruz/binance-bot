
from core.events import EventEmitter
from core.trade import TradeType

from core.database.collections.system import ResourceCollection, ResourceType, \
    ResourceStatus

resource_collection = ResourceCollection()


class Stratergy:

    trade_type = None
    __instances = {}

    def __new__(cls, **kwargs):
        ins = object.__new__(cls)
        # TODO hold up in memory?
        cls.__instances.update({ id(ins): ins })

        resource_collection.add(
            id=id(ins), 
            rtype=ResourceType.Stratergy, 
            status=ResourceStatus.Active
        )

        return ins

    def __init__(self, symbol, client, collection):
        self.symbol = symbol
        self.client = client
        self.collection = collection
        self.event = EventEmitter()
        assert self.trade_type is not None, 'Stratergy must define a trade type'

        # TODO register operation


    def __del__(self):
        resource_collection.destroy(id=id(self))

    def __call__(self):
        print("*** Running stratergy ***")

        # Pull all existing orders on the exchange and store in db
        self.sync_from_exchange()
        # Scalping processing - price action base 
        self.execute_action()

    def sync_from_exchange(self):
        # fetch data from exchange
        raise NotImplementedError

    def execute_action(self):
        # initial process run
        raise NotImplementedError

    @staticmethod
    def get_instance(id):
        return Stratergy.__instances.get(id)

    @staticmethod
    def get_instances(ttype: TradeType = None):
        if not ttype:
            return Stratergy.__instances.values()
        return [s for s in Stratergy.__instances.values() if s.trade_type == ttype]

    @staticmethod
    def run_all(ttype: TradeType = None):
        # TODO run all async
        for stratergy in Stratergy.get_instances(ttype):
            stratergy()